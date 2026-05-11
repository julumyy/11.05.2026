import pytest
from src.manager import Manager
from src.models import Parameters

def test_total_due_pln():
    params = Parameters(
        apartments_path='data/apartments.json',
        bills_path='data/bills.json',
        tenants_path='data/tenants.json',
        transfers_path='data/transfers.json'
    )

    manager = Manager(parameters=params)
    manager.load_data()

    apartment_key='apart-polanka'
    year=2025
    month=1

    apartment_costs = manager.get_apartment_costs(apartment_key, year, month)

    apt_settlement = manager.get_settlement(apartment_key, year, month)
    tenants_settlements = manager.create_tenants_settlements(apt_settlement)

    total_billed = sum(tenant_settlement.total_due_pln for tenant_settlement in tenants_settlements)

    assert total_billed == pytest.approx(apartment_costs, abs=0.01), f"Niezgodnosc dla {total_billed}: koszty={apartment_costs}, lokatorzy={tenants_settlements} "

def test_get_debtors():
    params = Parameters(
        apartments_path='data/apartments.json',
        bills_path='data/bills.json',
        tenants_path='data/tenants.json',
        transfers_path='data/transfers.json'
    )

    manager = Manager(parameters=params)
    manager.load_data()

    apartment_key='apart-polanka'
    year=2025
    month=1

    debtors = manager.get_debtors('apart-polanka', 1, 2025)
    assert len(debtors) > 0
    for debtor in debtors:
        assert debtor.total_transfers_pln < debtor.total_due_pln
    

def test_get_annual_report():
    params = Parameters(
        apartments_path='data/apartments.json',
        bills_path='data/bills.json',
        tenants_path='data/tenants.json',
        transfers_path='data/transfers.json'
    )

    manager = Manager(parameters=params)
    manager.load_data()

    report = manager.get_annual_report(2025)

    assert report is not None
    assert 'total_costs' in report
    assert 'total_income' in report
    assert report['total_costs'] >= 0

def test_data_integrity_costs_vs_settlements():
    
    from src.manager import Manager
    from src.models import Parameters
    params = Parameters(
        apartments_path='data/apartments.json',
        bills_path='data/bills.json',
        tenants_path='data/tenants.json',
        transfers_path='data/transfers.json'
    )

    manager = Manager(parameters=params)
    manager.load_data()

    apartment_key='apart-polanka'
    year=2025
    month=1

    settlement = manager.get_settlement(apartment_key, year, month)
    total_apartment_costs = settlement.total_due_pln

    tenant_reports = manager.create_tenants_settlements(settlement)
    total_tenants_due = sum(tenant_settlement.total_due_pln for tenant_settlement in tenant_reports)

    assert total_tenants_due == pytest.approx(total_apartment_costs)