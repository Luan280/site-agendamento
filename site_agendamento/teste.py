from datetime import datetime
import calendar
# Create your views here.
def calendar_view():
    data_obj = datetime.strptime("2025-04-07", "%Y-%m-%d").date()
    weekday = [
    "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado",
    "Domingo"
    ]
    date = data_obj.weekday()
    print(weekday[date])

if __name__ == '__main__':
    print(calendar_view())