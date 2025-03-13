import io
import matplotlib.pyplot as plt



async def create_plan_graph(plan: list, actual: list = None) -> io.BytesIO:
    """Создает график плана снижения курения и возвращает его как BytesIO объект"""
    # Очищаем все предыдущие фигуры
    plt.clf()
    plt.close('all')
    
    days = list(range(len(plan)))
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(days, plan, label="План", marker="o", linestyle="-", color="blue")
    
    if actual and len(actual) > 0:
        ax.plot(days[:len(actual)], actual, label="Факт", marker="x", linestyle="--", color="red")
    
    # Настраиваем оси
    ax.set_xticks(days)  # Показываем все дни на оси X
    max_cigarettes = max(plan)
    ax.set_ylim(0, max_cigarettes + 1)  # Устанавливаем диапазон оси Y
    ax.set_yticks(range(0, max_cigarettes + 1))  # Показываем все значения на оси Y
    
    ax.set_xlabel("День")
    ax.set_ylabel("Количество сигарет")
    ax.set_title("График снижения количества сигарет")
    ax.legend()
    ax.grid(True)
    
    # Сохраняем график в байтовый объект
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=300)
    buf.seek(0)
    
    # Закрываем фигуру
    plt.close(fig)
    
    return buf