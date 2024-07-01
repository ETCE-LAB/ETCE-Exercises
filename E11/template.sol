// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

contract EnergyTrading {

    struct Offer {
        uint offerID;
        uint amountToSell;
        uint pricePerUnit;
        bool isOpen;
    } // This is just an example of what information your smart contract will contain

    Offer[] public offerlist; // A publicly visible list of current and past offers

    constructor()  {
    }
    // Empty constructor (It is not really necessary to have anything in the constructor)

    function createOffer(uint _offerID, uint _amountToSell, uint _pricePerUnit) public {
	// you can leave the arguments the same

	// Initialize a new Offer object in the EVM memory

	// Push this new Offer object into the offerlist.
    }

    function listOffers() public view returns (Offer[] memory) {
        return offerlist;
    } // Just a function that lets you see the list of current and past offers

     function buyEnergy(uint _offerID) public payable returns (bool) {

        // Find the offer object based on the OfferID

	// Check if the amount of Ethereum spent in the transaction (msg.value) is at least as much as the required amount for purchasing this Offer (amountToSell * pricePerUnit)

	// If true, set isOpen to false

	// Return true if the transaction worked succesfully, false otherwise


    }
}

