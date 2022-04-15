// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract SimpleStorage {
    uint256 public favoriteNumber; // initialized to 0
    bool favoriteBool;
    /* Data types:
    bool favoriteBool = false;
    string favoriteString = "String";
    int256 = 5 or -5 ...
    address = 0x2374bB026d9af730F3EB8fCb76482e93F0e21040
    bytes32 favBytes = "cat"; // max to bytes 32
    */
    struct People {
        uint256 favoriteNumber;
        string name;
    }

    People[] public people;
    mapping(string => uint256) public nameToFavNumber;

    //People public person = People({favoriteNumber:2, name:"pedro"});

    function store(uint256 _favoriteNumber) public returns (uint256) {
        favoriteNumber = _favoriteNumber;
        return _favoriteNumber;
    }

    function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }

    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People(_favoriteNumber, _name));
        nameToFavNumber[_name] = _favoriteNumber;
    }
}
