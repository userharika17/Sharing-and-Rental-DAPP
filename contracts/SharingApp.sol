// SPDX-License-Identifier: MIT
pragma solidity 0.8.19;

contract SharingApp {
    struct Object {
        string name;
        string description;
        uint256 price;
        address owner;
        address renter;
        uint256 rentalStartTime;
    }

    mapping (uint => Object) public objects;
    uint256 public objectCount;

    function register_object(string memory _objectName, string memory _objectDescription, uint256 _objectPrice) public {
        objectCount++;
        objects[objectCount] = Object(_objectName, _objectDescription, _objectPrice, msg.sender, address(0), 0);
    }

    function rent_object(uint256 _objectId) public payable {
        require(objects[_objectId].owner != msg.sender, "You cannot rent your own object");
        require(objects[_objectId].renter == address(0), "Object is already rented");
        require(msg.value >= objects[_objectId].price, "Insufficient funds");

        objects[_objectId].renter = msg.sender;
        objects[_objectId].rentalStartTime = block.timestamp;

        payable(objects[_objectId].owner).transfer(msg.value);
    }

    function return_object(uint256 _objectId) public {
        require(objects[_objectId].renter == msg.sender, "You are not the renter of this object");

        objects[_objectId].renter = address(0);
        objects[_objectId].rentalStartTime = 0;
    }

    function getObjects() public view returns (address[] memory) {
        address[] memory objectOwners = new address[](objectCount);
        for (uint256 i = 1; i <= objectCount; i++) {
            objectOwners[i - 1] = objects[i].owner;
        }
        return objectOwners;
    }
}
