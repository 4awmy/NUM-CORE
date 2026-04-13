import os
import sys

def main_menu():
    print("=========================================")
    print("      NUMERICAL COMMAND CENTER v1.0      ")
    print("=========================================")
    print("[1] ROOT FINDER (Newton / Simple Iter)")
    print("[2] NETWORK SOLVER (Gauss-Seidel / Jacobi)")
    print("[3] DATA INTERPOLATOR (Newton / Lagrange)")
    print("[4] CALCULUS ENGINE (Integration / Diff)")
    print("[5] MISSION LAUNCH (Dashboard) <--- 'launch'")
    print("[Q] QUIT")
    print("=========================================")

def main():
    while True:
        main_menu()
        choice = input("NCC-Terminal> ").strip().lower()
        
        if choice == '1':
            print("[INFO] Loading Root Finder module...")
        elif choice == '2':
            print("[INFO] Loading Network Solver module...")
        elif choice == '3':
            print("[INFO] Loading Data Interpolator module...")
        elif choice == '4':
            print("[INFO] Loading Calculus Engine module...")
        elif choice == '5' or choice == 'launch':
            print("[SYSTEM] Initializing NCC Graphical Interface...")
            # subprocess.run(["python", "dashboard.py"])
        elif choice == 'q':
            print("Goodbye.")
            break
        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()
