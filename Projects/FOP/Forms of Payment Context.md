Pull form of payment based on context
Client card is segment specific
Compleat - applies policies and validation, then does final ticketing
Car rental doesn't use the on file cards. Must pay in person.
Can have secondary forms of payment for out of policy upgrades
CardsController??
Virtual Cards - Virtual card controller - used for hotels, stipends
Context will be segment specific
wallet controller is where the changes are needed
confermo virtual cards


Cards endpoint should combine wallets from personal and client

As a travel manager, I want to be able to specify 1 card for specific types of expenses for all travel

Sometimes I will have a choice of cards per segments, but that isn't the norm

1. Card attribute store - may be handled by the arranger stuff? 
2. Card endpoint - based on context - used by checkout flow and red app
3. UI for storing cards and attribute - settings page, cards page
4. Checkout page