# Reusable Three.js player and environment workflow

Source project: fluxoryid/wheres-my-pet. User requested retaining this process for other projects on 2026-11-08. This is a transferable implementation guide, not a claim of photorealism or a deployment instruction.

## Player model and gait

Use metres consistently: adult height about 1.8 m, hip centre about 0.94 m, hip spacing about 0.17 m. Keep the torso upright. Build nested shoulder/arm and hip/thigh/knee/shin/foot groups. Place each pivot at its anatomical joint, not the centre of its mesh. Forward is local +Z, up is +Y. Rotate legs in the sagittal plane (local X axis); avoid sideways Z rotation that produces a splayed stance. Give upper legs a restrained ±0.30 rad swing, arms an opposing ±0.20 rad swing, and bend the knees during swing, reaching approximately 0.68 rad. Offset right and left phases by half a cycle. Preserve identical loop endpoints. These values are a starting point; inspect heel strike, toe off, ground contact and foot sliding from front and side views before accepting the animation. A production gait should use foot-locking/IK or motion capture when available.

Export named quaternion tracks in the GLB Walk clip. Keep idle upright and blend action weight to zero when stationary. Drive playback from actual displacement and align actor yaw to movement direction; cap speed to avoid jitter from network snapshots. Reset motion when spawning or teleporting. Clone actors independently; skeletal meshes need SkeletonUtils.clone. Never dispose shared cached geometry when removing a single actor.

Reference: scripts/build-models.mjs (human, humanWalk, --humans-only), dist/world.js (makePlayer / update), dist/assets.js (NPC playback). Rebuild only affected assets; retain the source builder alongside generated GLBs.

## Materials and textures

Use MeshStandardMaterial / MeshPhysicalMaterial with named material families. Color/albedo textures use SRGBColorSpace; normal and roughness maps use NoColorSpace. Use deterministic, repeatable noise, mipmaps and modest anisotropy; separate wood grain, fabric weave, stone/concrete grain, asphalt and tile joints. Normals must be encoded from normalized vectors, not from an RGB albedo image. Roughness should vary independently of base color. Avoid adding grain to glass or assuming all surfaces are metallic. Use measured, properly licensed albedo/normal/roughness assets with correct real-world UV scale for photorealistic work. Procedural microtextures add detail but cannot replace high quality geometry or photographic PBR scans.

Reference: dist/materials.js. Reuse generated texture maps rather than allocating per object, and preserve source-asset maps. Batch instances by material family, not all materials together. Tune tiling to dimensions; the current game's normalized building UVs are a remaining realism limit.

## Lighting and shadows

Use an HDR/PMREM environment for image-based lighting and reflections, a restrained sky/hemisphere fill, and one key sun/moon directional light. Change sky tint, intensity, exposure and reflection environment consistently with time of day. Work in linear lighting, then tone map once for display.

Emissive lenses alone do not illuminate nearby surfaces. Pair visible lamp, window, headlight and taillight materials with actual lights. Street and entry lamps point downward; vehicle headlights follow local forward direction with a small downward pitch. Use inverse-square attenuation (decay 2), finite range, a soft spotlight penumbra, and matching color temperature. Maintain a fixed nearby light pool to bound shader cost; keep fixture metadata for the entire world, select nearby sources periodically, and move assigned vehicle lights each frame. Limit shadowed lights separately from visible lights. The game currently uses 12 spotlight slots and 2 shadow-casting nearby slots; this is an explicit performance compromise, not every lamp simultaneously illuminating the entire map. Add fixture types for motorcycles or other vehicles only when those objects exist in the target project.

Use sun shadow coverage around the player, a tight camera frustum, appropriate shadow near/far planes and normal bias; balance acne against detached contact shadows. Local shadow maps use 512px; main sunlight uses 2048px. Disable or reduce costly shadows on distant foliage before sacrificing character contact shadows. Dispose shadow targets and remove light targets on teardown.

Reference: dist/lighting.js, dist/world.js updateDay/setupEnvironment, dist/assets.js emissive updates. Building exterior spill is currently represented by entry lights and emissive windows, not a physically simulated interior behind every window. Reflections are PMREM environment reflections; dynamic screen-space / planar / ray-traced reflections are separate features.

## Verification and portability

1. Inspect the target engine revision, asset licences, model axes, units, and mobile/GPU budget before copying implementation.
2. Run repository tests and add behavioural regression tests for gait articulation, standing idle, light placement/direction, time-of-day dimming, pooling limits and teardown.
3. Render a character from front/side at key gait phases. Render day/night surface patches beneath street lamps, beside facades and in front of cars. Inspect shadows and surface normals. Exercise movement and idle transitions in a real browser.
4. Measure frame time, draw calls, triangle counts and memory on hardware and software renderers. Keep diagnostic overrides out of production code.
5. Report initialization checks separately from interactive gameplay and visual acceptance. Software WebGL in this cloud environment previously timed out on continuous city rendering; animation-paused bootstrap success does not prove gameplay or photorealism.

This file persists in this workspace. No cross-project global memory tool was available when it was written; carry this guide into the next project's context to reuse it.
