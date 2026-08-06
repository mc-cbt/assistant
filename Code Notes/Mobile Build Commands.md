# Mobile Build Commands

Build commands for `traveler-mobile` in the [[Code Notes/Andavo Repo — Local Layout & Worktrees|Andavo repo]].

## Full iOS rebuild

Only needed when native code or pods change:

```bash
rm -rf apps/traveler-mobile/ios
bun nx run traveler-mobile:prebuild --platform ios --install=false
bun nx run traveler-mobile:fix-ios-platforms
(cd apps/traveler-mobile/ios && pod install)
bun nx run traveler-mobile:run-ios --install=false --device "iPhone 17 Pro"
```

## JS / UI work

None of the above is needed — just start the dev server:

```bash
bun nx start traveler-mobile
```
