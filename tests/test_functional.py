import pytest
from src.manager import Manager
from src.models import Parameters

def total_due_pln():
    manager = Manager(Parameters())
    costs = manager.get_apartment_costs('apartment-1', 2024, 1)
    assert costs is None

    costs = manager.get_apartment_costs('apart-polanka', 2024, 1)
    assert costs == 0.0

    costs = manager.get_apartment_costs('apart-polanka', 2025, 1)
    assert costs == 910.0

    with pytest.raises(ValueError):
        manager.get_apartment_costs('apart-polanka', 2024, 13)
        manager.get_apartment_costs('apart-polanka', 2024, 0)

def test_get_debtors():
    manager = Manager(Parameters())
    debtors = manager.get_debtors('apartment-1', 1, 2024)
    assert debtors is None

    debtors = manager.get_debtors('apart-polanka', 1, 2024)
    assert debtors == []

    debtors = manager.get_debtors('apart-polanka', 1, 2025)
    assert debtors == []
    

def test_get_annual_report():
    manager = Manager(Parameters())
    annual_report = manager.get_annual_report(2024)
    assert annual_report is not None
    assert annual_report['apart-polanka'] is None

    annual_report = manager.get_annual_report(2025)
    assert annual_report is not None
    assert annual_report['apart-polanka'] == 910.0

    with pytest.raises(ValueError):
        manager.get_annual_report(2024)
        manager.get_annual_report(2025)