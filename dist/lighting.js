import * as T from './vendor/three.module.js';
// Fixed shader light count. Only the closest fixtures consume actual light slots.
export class CityLighting {
 constructor(scene){
  this.scene=scene;this.sources=[];this.lastSelection=-Infinity;
  this.spots=Array.from({length:12},(_,i)=>{
   const light=new T.SpotLight(0xffe0ad,0,42,Math.PI/3,.55,2);
   light.castShadow=i<2;light.shadow.mapSize.set(512,512);
   light.shadow.bias=-.0003;light.shadow.normalBias=.06;
   light.shadow.camera.near=.2;light.shadow.camera.far=65;
   scene.add(light,light.target);return light;
  });
 }
 rebuild(world){
  this.sources=world.lights.map(p=>({kind:'street',position:new T.Vector3(p.x+1.2,7,p.z),direction:new T.Vector3(0,-1,0),power:650,color:0xffdfaa,distance:34,angle:Math.PI*.36}));
  const buildings=new Map();for(const e of world.static)if(e.record.type==='building'&&(!buildings.has(e.record)||buildings.get(e.record).h<e.h))buildings.set(e.record,e);
  for(const [record,e] of buildings){
   this.sources.push({kind:'entry',position:new T.Vector3(record.x,3,record.z+e.d/2+.8),direction:new T.Vector3(0,-1,.3).normalize(),power:230,color:0xffcf91,distance:16,angle:Math.PI/3});
  }
  const truck=world.m.truck;
  this.sources.push({kind:'truck',position:new T.Vector3(truck.x,1.25,truck.z+3),direction:new T.Vector3(0,-.08,1).normalize(),power:1100,color:0xe9f2ff,distance:55,angle:.38});
  this.lastSelection=-Infinity;
 }
 update(world,t,local){
  const night=world.day==='Malam',dusk=world.day==='Sore',strength=night?1:dusk?.55:0;
  if(t-this.lastSelection>.4){
   this.lastSelection=t;
   const candidates=this.sources.map(source=>({...source,d:Math.hypot(source.position.x-local.x,source.position.z-local.z)}));
   for(const car of world.traffic){
    const x=car.axis==='x'?car.offset:car.lane+car.dir*4.5,z=car.axis==='z'?car.offset:car.lane+car.dir*4.5;
    if(Math.abs(x-world.plan.river)<39&&![-450,-150,150,450].some(v=>Math.abs(z-v)<10))continue;
    const direction=new T.Vector3(car.axis==='x'?car.dir:0,-.08,car.axis==='z'?car.dir:0).normalize();
    candidates.push({kind:'headlight',position:new T.Vector3(x+direction.x*2.2,.52,z+direction.z*2.2),direction,power:950,color:0xe9f2ff,distance:55,angle:.36,d:Math.hypot(x-local.x,z-local.z),car});
   }
   candidates.sort((a,b)=>a.d-b.d);
   this.selected=candidates.filter(s=>s.d<85).slice(0,this.spots.length);
  }
  this.spots.forEach((light,i)=>{
   const s=this.selected?.[i];light.intensity=s?s.power*strength:0;
   if(!s)return;
   // Headlights follow their vehicle every frame, including turns at wraparound.
   if(s.car){const c=s.car;s.position.set(c.axis==='x'?c.offset:c.lane+c.dir*4.5,.52,c.axis==='z'?c.offset:c.lane+c.dir*4.5);s.position.addScaledVector(s.direction,2.2)}
   light.position.copy(s.position);light.target.position.copy(s.position).add(s.direction);
   light.color.set(s.color);light.distance=s.distance;light.angle=s.angle;
   light.target.updateMatrixWorld();
  });
 }
 dispose(){for(const l of this.spots){this.scene.remove(l,l.target);l.shadow.map?.dispose()}this.sources=[]}
}
