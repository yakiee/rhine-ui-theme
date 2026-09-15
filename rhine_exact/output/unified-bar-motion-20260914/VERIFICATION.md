# Bottom bar motion consistency — 2026-09-14

Applied through the official KLWP editor on the physical Xiaomi HyperOS phone.

## Change

The bottom plate, battery/date layer, and glow each contained two terminal-specific position animations in addition to launcher scrolling: a 90-point downward offset and a second offset ending at 720 points. Leaving the terminal page reversed these timed animations while the launcher scroll animation was also changing position and angle.

For all three components, the two terminal geometry animations were replaced by one identical 3.2-unit FADE animation. The launcher SCROLL keyframes, pivot, layout, gyro, resources, and battery/date scroll fade were retained. Terminal visibility therefore no longer adds a different trajectory to the bar.

## Applied animation counts

- Plate: 5 → 4.
- Battery/date: 6 → 5.
- Glow: 5 → 4.

Native editor lists were checked after each paste. Root modules were not replaced or reordered. Existing page visibility and WeChat fixes were not edited.

The final theme was saved, KLWP restarted, and the wallpaper re-applied to the home screen only to avoid the previously observed post-save opacity issue.

## Validation

- Captured 1.8-second drags from page 2 to page 3 and back, first with terminal closed, then open.
- Compared starting, intermediate, and settled frames in the closed-away, closed-return, opened-away, and opened-return PNG sequences.
- Neighboring-page bar placement matched; the former large terminal-specific downward/reverse displacement was absent in the sampled frames.
- Returning to page 2 restored the diagonal plate, glow and battery/date.
- Opening the terminal hid the complete bottom bar; terminal buttons remained visible.

This does not claim identical brightness during transitions: the terminal intentionally controls the shared fade. Geometry follows the same existing launcher scroll trajectory in both states.
