# backend/tools.py

def calculate_speed_fine(
    posted_limit: int,
    actual_speed: int
):

    difference = actual_speed - posted_limit

    if difference <= 10:
        fine = 500

    elif difference <= 20:
        fine = 1000

    elif difference <= 40:
        fine = 2000

    else:
        fine = 5000

    return f"""
Overspeed Fine:
Posted Limit = {posted_limit}
Actual Speed = {actual_speed}
Fine = ₹{fine}
"""


def mock_toll_wallet_deduction(
    vehicle_id: str,
    total_fine: int
):

    return f"""
Wallet deduction successful.

Vehicle ID:
{vehicle_id}

Amount Deducted:
₹{total_fine}
"""