require("@nomiclabs/hardhat-waffle");

module.exports = {
  solidity: "0.8.23",
  networks: {
    hardhat: {
      // No "forking" here; we'll pass --fork on the CLI instead
    }
  }
};
