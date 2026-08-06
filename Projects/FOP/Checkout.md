# Checkout

Notes on the FOP checkout flow — open questions, decided behavior, and TODOs.

## Open questions

- Need to open up / figure out the endpoint for calculating the trip name.
- If a traveler chooses **not** to save the card, how does the card get saved? Do we always add it to their profile? If not, just apply it to the booking only without saving it to the wallet.

## Decided behavior

- Clicking **Purchase** opens the trip attribute sheet if attributes still need to be captured.
- Clicking the **payment button** also opens the attribute sheet if needed.
- Should we disallow personal cards in the checkout flow? **No, not for now.**

## TODO

- Always collect UDIDs, even when they aren't linked to payment methods.
