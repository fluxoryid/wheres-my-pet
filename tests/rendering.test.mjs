import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import * as T from '../dist/vendor/three.module.js';
import {GLTFLoader} from '../dist/vendor/GLTFLoader.js';
import {CityLighting} from '../dist/lighting.js';
import {enhanceMaterial,updateEmission} from '../dist/materials.js';
test('human gait articulates knees in the forward plane with narrow hip spacing',async()=>{
 for(const name of ['human-male','human-female']){
  const bytes=await fs.readFile(new URL('../dist/models/'+name+'.glb',import.meta.url));
  const asset=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');
  const left=asset.scene.getObjectByName('leg_l'),right=asset.scene.getObjectByName('leg_r');
  assert.ok(right.position.x-left.position.x<.19);
  assert.equal(asset.scene.getObjectByName('shin_l').parent,left);
  assert.equal(asset.scene.getObjectByName('shin_r').parent,right);
  const mixer=new T.AnimationMixer(asset.scene),action=mixer.clipAction(asset.animations[0]);action.play();
  let maxFlex=0;
  for(let i=0;i<=32;i++){
   mixer.setTime(i/32);const shin=asset.scene.getObjectByName('shin_l');maxFlex=Math.max(maxFlex,Math.abs(shin.rotation.x));
   for(const leg of [left,right]){assert.ok(Math.abs(leg.rotation.z)<1e-5);assert.ok(Math.abs(leg.rotation.y)<1e-5);assert.ok(Math.abs(leg.rotation.x)<=.31)}
   assert.ok(Math.abs(asset.scene.getObjectByName('torso').rotation.z)<1e-5);
  }
  assert.ok(maxFlex>.6);
  action.setEffectiveWeight(0);mixer.update(.1);assert.ok(Math.abs(left.rotation.x)<1e-5);
 }
});
function fixture(){const scene=new T.Scene(),lighting=new CityLighting(scene);const world={lights:[{x:0,z:0}],static:[],m:{truck:{x:200,z:200}},traffic:[],plan:{river:300},day:'Malam'};lighting.rebuild(world);return{scene,lighting,world}}
test('street lamps light downward, dim by day, and keep a bounded reusable light pool',()=>{
 const {scene,lighting,world}=fixture();lighting.update(world,0,{x:0,z:0});const lamp=lighting.spots[0];assert.ok(lamp.intensity>0);assert.ok(lamp.target.position.y<lamp.position.y);assert.equal(lamp.decay,2);
 const initial=scene.children.length;for(let t=1;t<10;t++)lighting.update(world,t,{x:t,z:0});assert.equal(scene.children.length,initial);assert.equal(lighting.spots.filter(l=>l.castShadow).length,2);
 world.day='Siang';lighting.update(world,11,{x:0,z:0});assert.ok(lighting.spots.every(l=>l.intensity===0));lighting.dispose();assert.equal(scene.children.length,0);
});
test('headlights follow moving vehicles and their direction of travel',()=>{
 const {lighting,world}=fixture();world.lights=[];world.traffic=[{axis:'x',offset:10,lane:0,dir:-1}];lighting.rebuild(world);lighting.update(world,0,{x:10,z:0});const light=lighting.spots[0];assert.ok(light.intensity>0);assert.ok(light.target.position.x<light.position.x);const before=light.position.x;world.traffic[0].offset-=2;lighting.update(world,.1,{x:10,z:0});assert.ok(light.position.x<before);lighting.dispose();
});
test('PBR details use separate linear normal/roughness and sRGB albedo; lenses glow at night',()=>{
 const wood=enhanceMaterial(new T.MeshStandardMaterial({name:'wood'}));assert.equal(wood.map.colorSpace,T.SRGBColorSpace);assert.equal(wood.normalMap.colorSpace,T.NoColorSpace);assert.notEqual(wood.normalMap,wood.map);assert.ok(wood.roughnessMap);
 const head=enhanceMaterial(new T.MeshStandardMaterial({name:'headlight'}));updateEmission(head,true);const night=head.emissiveIntensity;updateEmission(head,false);assert.ok(night>head.emissiveIntensity);
});
