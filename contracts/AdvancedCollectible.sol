// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
//import "@chainlink/contracts/src/v0.8/VRFV2WrapperConsumerBase.sol";
import "@chain/contracts/src/v0.8/vrf/VRFV2WrapperConsumerBase.sol";

contract AdvancedCollectible is ERC721URIStorage, VRFV2WrapperConsumerBase {
    uint256 public tokenCounter;
    uint32 public callbackGasLimit;
    uint16 public requestConfirmations;
    uint32 public numWords;
    enum Sky {
        CRESCENT,
        NEBULA,
        STARS
    }
    mapping(uint256 => Sky) public tokenIDtoSky;
    mapping(uint256 => address) public requestIDtoSender;
    event requestedCollectible(uint256 indexed requestID, address requester);
    event skyAssigned(uint256 indexed tokenID, Sky sky);

    constructor(
        address wrapperAddress,
        address linkAddress,
        uint32 _callbackGasLimit,
        uint16 _requestConfirmations,
        uint32 _numWords
    )
        VRFV2WrapperConsumerBase(linkAddress, wrapperAddress)
        ERC721("Jerma", "JEX")
    {
        tokenCounter = 0;
        callbackGasLimit = _callbackGasLimit;
        requestConfirmations = _requestConfirmations;
        numWords = _numWords;
    }

    function createCollectible() public returns (uint256) {
        uint256 requestId = requestRandomness(
            callbackGasLimit,
            requestConfirmations,
            numWords
        );
        requestIDtoSender[requestId] = msg.sender;
        emit requestedCollectible(requestId, msg.sender);
    }

    function fulfillRandomWords(
        uint256 _requestId,
        uint256[] memory _randomWords
    ) internal override {
        Sky sky = Sky(_randomWords[0] % 3);
        uint256 newTokenID = tokenCounter;
        tokenIDtoSky[newTokenID] = sky;
        emit skyAssigned(newTokenID, sky);
        address owner = requestIDtoSender[_requestId];
        _safeMint(owner, newTokenID);
        tokenCounter = tokenCounter + 1;
    }

    function setTokenURI(uint256 tokenID, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), tokenID),
            "ERC721 caller is not owner nor approved"
        );
        _setTokenURI(tokenID, _tokenURI);
    }
}
