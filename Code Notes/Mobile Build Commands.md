
Your go-to command for future rebuilds (only needed when native code/pods change):
rm -rf apps/traveler-mobile/ios
bun nx run traveler-mobile:prebuild --platform ios --install=false
bun nx run traveler-mobile:fix-ios-platforms
(cd apps/traveler-mobile/ios && pod install)
bun nx run traveler-mobile:run-ios --install=false --device "iPhone 17 Pro"
For pure JS/UI work you won't touch any of that — just bun nx start traveler-mobile.