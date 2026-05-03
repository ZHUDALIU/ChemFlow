#!/usr/bin/env python3
"""ChemFlow demo: input generation, error diagnosis, and healing workflow."""

import sys
import os

# Ensure project root is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chemflow.input_master import InputMaster
from chemflow.heal_master import HealMaster, Status


def main() -> None:
    print("=" * 60)
    print("  ChemFlow - Computational Chemistry Workflow Assistant")
    print("  LLM-Powered | Gaussian Input Generation & Error Healing")
    print("=" * 60)

    # Step 1: Generate input file
    print("\n  [Step 1] Generating Gaussian input file for Aspirin...")
    master = InputMaster()
    gjf_content = master.generate("aspirin", "B3LYP", "6-31+G(d,p)", "Opt")

    print("\n" + "-" * 60)
    print("  [ aspirin_opt.gjf ]")
    print("-" * 60)
    print(gjf_content)
    print("-" * 60)

    # Step 2: Simulate calculation failure
    print("  [Step 2] Submitting Gaussian calculation... (simulated)")
    print("  Job submitted ... waiting for results ...")

    print("\n  [Step 3] Calculation failed! Analyzing output log...")
    simulated_log = """
 Gaussian 16: ES64L-G16RevC.01
 -------------------------------------------------------------
                           Input file
 -------------------------------------------------------------
 %chk=aspirin.chk
 # Opt B3LYP/6-31+G(d,p)

 Title: Aspirin Opt at B3LYP/6-31+G(d,p)

 0 1
 C    0.000000    0.000000    0.000000
 ...

 -------------------------------------------------------------
 SCF Done:  E(RB3LYP) = -648.321045909     A.U. after   12 cycles
 Convergence failure in SCF iteration
 -------------------------------------------------------------
    """

    print("\n" + "-" * 60)
    print("  Gaussian Output Log (simulated)")
    print("-" * 60)
    print(simulated_log)
    print("-" * 60)

    healer = HealMaster()
    status = healer.diagnose(simulated_log)
    print("  [DIAGNOSIS] Status: " + status.value.upper())

    # Step 3: Heal
    print("\n  [Step 4] Healing input file...")
    healed = healer.heal(gjf_content, status)

    print("\n" + "-" * 60)
    print("  [ aspirin_opt_healed.gjf ]")
    print("-" * 60)
    print(healed)
    print("-" * 60)

    # Summary
    print("\n  [Step 5] Summary")
    print("  [OK] Original input successfully generated")
    print("  [DIAGNOSIS] " + status.value)
    print("  [FIX] Applied fixes: scf=xqc + int=ultrafine")
    print("  [OK] Healed input ready for resubmission")
    print("=" * 60)


if __name__ == "__main__":
    main()