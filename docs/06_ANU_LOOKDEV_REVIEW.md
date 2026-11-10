# Anu look-development review — Exploration v0.1

**Date:** 2026-11-11
**Status (updated 2026-11-11):** CURRENT LOOK APPROVED IN PRINCIPLE / SOURCE PIXELS NOT RECOVERED / NOT MODELED
**Historical review:** sections below retain the v0.1 study notes; they are not a new pixel inspection. [Reference control v0.2](07_ANU_REFERENCE_LOCK.md) governs the current gate.
**Owner review required before:** character proportion lock, costume lock, facial rig, final model.
**Generated review sheets:** `anu_turnaround_exploration_v01.png` and `anu_expressions_exploration_v01.png` were made as conversation attachments; **not yet committed** to GitHub. They are visual proposals, not canonical asset files.

## 1. Hard requirements (already established)
- Anu is **five years old**, South Indian, curious, playful and emotionally spontaneous.
- **Messy shoulder-length dark hair**.
- **Yellow butterfly hair clip** with visible, recognizable silhouette.
- Natural complete front teeth: **no missing front tooth**.
- Child anatomy and movement, not scaled-down adult proportions.
- The film never depends on Anu giving a grown-up explanation of grief.

## 2. First generated design: candidate details only
- Round, soft facial construction; thick dark eyebrows; dark expressive eyes; choppy loose hair strands.
- Sunshine-yellow printed dress, light shoes, and small bunny crossbody bag: **entirely speculative wardrobe/accessory options**.
- A four-view turnaround (front / three-quarter / side / back) and expression studies.
- The generated board included an approximate height annotation; **height is not confirmed and should not be imported into modeling specs**.
- Facial identity, skin appearance, proportions and clip orientation must be checked for continuity across every view. Generated images are illustration, not geometry-ready orthographic blueprints.

## 3. What currently works
1. Instantly identifiable yellow butterfly clip.
2. Gentle painterly skin and hair, with a childlike silhouette.
3. Readable transitions between curiosity, excitement and disappointment.
4. Attractive tactile look that could be approached with subtle shaders and a stylized lighting setup.

## 4. Fixes to investigate before approval
- Reduce stylization if large eyes, shiny materials or a strongly 'toy' face undermine believable acting.
- Ensure exact same head shape, ear position, hair outline and clip position across the front, profile and back views.
- Verify child anatomy in silhouette and motion; avoid rigid fashion poses.
- Explore wardrobe color separation from the butterfly clip. The printed dress and bunny bag are **not mandatory** and could be replaced.
- Add essential low-intensity expressions: tentative hope, hesitation, focused concentration, disbelief and quiet hurt; avoid only exaggerated cartoon faces.
- Confirm natural proportion of teeth in open-mouth expressions.
- Test character readability under **daylight, dim room light and gentle bounce light**—not only idealized promotional golden hour.

## 5. Animation requirements to design for
- Facial controls: brows, gaze, blinks, eyelid compression, cheek motion, subtle mouth corners, breathing and small involuntary movements.
- Expression targets: **curious, delighted, mischievous, focused, hopeful, confused, disappointed, quietly sad, comforted**.
- Full-body actions: crouch/stand, scamper, reach, lean into a hug, hold an object, play with hands, step back, pause and hesitate.
- Hair: simple groom or cards with secondary motion; no expensive simulations until render benchmark.
- Outfit: deformation-friendly fabric and folds; no fragile high-poly detail that hampers animation.
- Scale check: home props, furniture and door handles must feel correct from a five-year-old's eye level.

## 6. Rejected incidental content in generated mood boards
Two larger AI mood boards included invented stories (fantasy castle/portals, definitive final tree, invented precise character ages, full portrait/reveal of Amma and alternate family roles). These **are not approved and do not override** `00_STORY_CANON.md`. Particularly, Amma must **not** become a fully shown present-time or memory character, and the story must not become a fantasy-portal adventure.

## 7. Required approval gate
Before 3D modeling, review:
- [ ] Confirm face/head/hair direction
- [ ] Confirm child proportions
- [ ] Confirm outfit silhouette, accessory decision and material palette
- [ ] Confirm butterfly clip size, location and consistency
- [ ] Confirm 8–10 key expressions
- [ ] Choose/look-test a neutral, daylight and emotional-lighting reference
- [ ] Approve turnaround or request v0.2 revisions

**Immediate next milestone (updated):** recover and archive the exact original concept PNGs, inspect continuity, prepare a corrected modeling packet preserving the accepted look, then execute the bounded rig test. Approval in principle does not close the unchecked construction/costume gates.
