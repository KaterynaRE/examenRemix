import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";

export default buildModule("BankModule", (m) => {
  const calculator = m.contract("InterestCalculator", [5]);
  const bank = m.contract("DepositBank", [calculator]);

  return { bank, calculator };
});
