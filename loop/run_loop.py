"""Orchestrator — führt den täglichen Loop aus.
Reihenfolge: Agent 1 (Daten) → Agent 2 (Dashboard)
"""
import datetime
import agent1_data_qa, agent2_dashboard_qa
from lib import load_state, save_state, TODAY

def main():
    state = load_state()
    crit1 = agent1_data_qa.main()
    crit2 = agent2_dashboard_qa.main()
    state["last_run"] = TODAY
    state.setdefault("history", []).append(
        {"date": TODAY, "data_critical": crit1, "dashboard_critical": crit2})
    save_state(state)
    print("Loop fertig.")

if __name__ == "__main__":
    main()
