from datetime import datetime
import calendar
# Create your views here.
def calendar_view():
    """
    Exibe um calendário com todos os dias do mês atual.
    Ao clicar em um dia, mostra os horários disponíveis.
    """
    hoje = datetime.today()
    ano, mes = hoje.year, hoje.month
    meses= ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    # Pega o "nome" do mes, de acordo com o número do mes.['0': 'Janeiro', '1': 'Fevereiro']
    mes_atual = meses[mes -1]
    # Quantidade de dias do mês.
    total_dias_mes = calendar.monthrange(ano, mes)[1]
    lista_dias_mes = [dia for dia in range(1, total_dias_mes + 1)]
    return lista_dias_mes

if __name__ == '__main__':
    print(calendar_view())