import * as T from './vendor/three.module.js';
const maps=new Map();
// Deterministic microstructure; no external downloads or random changes on reload.
function detail(kind){
 if(maps.has(kind))return maps.get(kind);
 const size=128,color=new Uint8Array(size*size*4),rough=new Uint8Array(size*size*4),normal=new Uint8Array(size*size*4);
 const height=(x,y)=>{const noise=Math.sin(x*127.1+y*311.7)*43758.5453;const n=noise-Math.floor(noise);
  if(kind==='wood')return .5+.25*Math.sin(x*.28+Math.sin(y*.06)*2)+n*.12;
  if(kind==='fabric')return .4+((x%3===0||y%3===0)?.25:0)+n*.1;
  if(kind==='tiles')return x%32<2||y%32<2?.12:.65+n*.12;
  return .35+n*.4;
 };
 for(let y=0;y<size;y++)for(let x=0;x<size;x++){
  const i=(y*size+x)*4,h=height(x,y),v=kind==='asphalt'?150+h*55:195+h*55;
  color.set([v,v,v,255],i);rough.set([180+h*65,180+h*65,180+h*65,255],i);
  const n=new T.Vector3((h-height(x+1,y))*.5,(h-height(x,y+1))*.5,1).normalize();normal.set([(n.x*.5+.5)*255,(n.y*.5+.5)*255,(n.z*.5+.5)*255,255],i);
 }
 const make=(data,srgb=false)=>{let t=new T.DataTexture(data,size,size);t.wrapS=t.wrapT=T.RepeatWrapping;t.repeat.set(kind==='fabric'?6:4,kind==='fabric'?6:4);t.colorSpace=srgb?T.SRGBColorSpace:T.NoColorSpace;t.generateMipmaps=true;t.minFilter=T.LinearMipmapLinearFilter;t.magFilter=T.LinearFilter;t.anisotropy=4;t.needsUpdate=true;return t};
 const result={map:make(color,true),roughnessMap:make(rough),normalMap:make(normal)};maps.set(kind,result);return result;
}
export function enhanceMaterial(material){
 if(material.userData.cityDetail)return material;
 material.userData.cityDetail=true;
 const name=material.name.toLowerCase();
 const kind=/wood|bark/.test(name)?'wood':/fabric|denim|canvas/.test(name)?'fabric':/roof/.test(name)?'tiles':/asphalt/.test(name)?'asphalt':/concrete|stone|foundation|ground|pavement/.test(name)?'concrete':null;
 if(kind&&!material.map){Object.assign(material,detail(kind));material.normalScale=new T.Vector2(.22,.22)}
 if(/glass|window/.test(name)){material.roughness=.16;material.metalness=.15;material.envMapIntensity=1.15}
 if(/headlight|^light$|lamp/.test(name)){material.emissive=new T.Color(0xffdda8);material.userData.nightEmission=3}
 if(/taillight/.test(name)){material.emissive=new T.Color(0xff2714);material.userData.nightEmission=2}
 if(/window/.test(name)){material.emissive=new T.Color(0xffc078);material.userData.nightEmission=.28}
 material.needsUpdate=true;return material;
}
export function updateEmission(material,night){if(material.userData.nightEmission!==undefined)material.emissiveIntensity=night?material.userData.nightEmission:.02}
