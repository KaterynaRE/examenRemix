import hardhat from "hardhat";

async function main() {
  const [deployer] = await hardhat.ethers.getSigners();

  console.log("Deploying with:", deployer.address);

  const DepositBank = await hardhat.ethers.getContractFactory("DepositBank");
  const bank = await DepositBank.deploy(
    deployer.address,
    hardhat.ethers.parseEther("100"),
    true,
    hardhat.ethers.parseEther("0.01")
  );
  await bank.waitForDeployment();

  console.log("DepositBank deployed at:", await bank.getAddress());

  const InterestCalculator = await hardhat.ethers.getContractFactory("InterestCalculator");
  const calculator = await InterestCalculator.deploy(5);
  await calculator.waitForDeployment();

  console.log("InterestCalculator deployed at:", await calculator.getAddress());

  await (await bank.setCalculator(await calculator.getAddress())).wait();
  console.log("Contracts linked");
}

main().catch(console.error);
