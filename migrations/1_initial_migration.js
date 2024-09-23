const SharingApp = artifacts.require("SharingApp");

module.exports = function(deployer) {
  deployer.deploy(SharingApp);
};