// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

contract SimpleCollectible is ERC721URIStorage {
    uint256 public tokenCounter;

    constructor() public ERC721("Jerma", "JEX") {
        tokenCounter = 0;
    }

    function createCollectible(
        string memory tokenURI
    ) public returns (uint256) {
        uint256 newTokenID = tokenCounter;
        _safeMint(msg.sender, newTokenID);
        _setTokenURI(newTokenID, tokenURI);
        tokenCounter = tokenCounter + 1;
        return newTokenID;
    }
}
