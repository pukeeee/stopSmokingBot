import io
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime



async def create_plan_graph(plan: list, actual: list = None) -> io.BytesIO:
    """Создает график плана снижения курения и возвращает его как BytesIO объект"""
    # Очищаем все предыдущие фигуры
    plt.clf()
    plt.close('all')
    
    # Настраиваем стиль
    plt.style.use('seaborn-v0_8-darkgrid')
    
    days = list(range(len(plan)))
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='#282A36')
    ax.set_facecolor('#44475A')
    
    # Основная линия плана
    ax.plot(days, plan, label="План", marker="o", linestyle="-", color="#F8F8F2", linewidth=2.5, 
            markersize=8, markerfacecolor="#F8F8F2", markeredgecolor="white", markeredgewidth=1.5)
    
    if actual and len(actual) > 0:
        ax.plot(days[:len(actual)], actual, label="Факт", marker="x", linestyle="--", color="#FF79C6", 
                linewidth=2.5, markersize=8, markeredgewidth=2)
    
    # Настраиваем оси
    ax.set_xticks(days)  # Показываем все дни на оси X
    max_cigarettes = max(plan)
    ax.set_ylim(0, max_cigarettes + 1)  # Устанавливаем диапазон оси Y
    ax.set_yticks(range(0, max_cigarettes + 1))  # Показываем все значения на оси Y
    
    # Стилизуем оси, подписи и сетку
    ax.set_xlabel("День", fontsize=12, fontweight='bold', color='#FF79C6')
    ax.set_ylabel("Кількість сигарет", fontsize=12, fontweight='bold', color='#FF79C6')
    ax.set_title("Графік зниження кількості сигарет", fontsize=14, fontweight='bold', color='#F8F8F2', pad=15)
    
    # Настраиваем сетку
    ax.grid(True, linestyle=':', alpha=0.5, color='#F8F8F2')
    
    # Настраиваем рамку графика
    for spine in ax.spines.values():
        spine.set_color('#F8F8F2')
        spine.set_linewidth(0.5)
    
    # Настраиваем подписи осей
    ax.tick_params(axis='both', colors='#6272A4', labelsize=10)
    
    # Настраиваем легенду
    legend = ax.legend(loc='upper right', frameon=True, framealpha=0.9, 
                       facecolor='#282A36', edgecolor='#F8F8F2')
    legend.get_frame().set_linewidth(1.5)
    
    # Устанавливаем цвет текста легенды на белый
    for text in legend.get_texts():
        text.set_color('#F8F8F2')
    
    # Добавляем аннотации для начального и конечного значений
    ax.annotate(f"{plan[0]}", (0, plan[0]), xytext=(0, plan[0]+0.5), 
                color='#FF79C6', fontweight='bold', ha='center')
    ax.annotate(f"{plan[-1]}", (len(plan)-1, plan[-1]), xytext=(len(plan)-1, plan[-1]+0.5), 
                color='#FF79C6', fontweight='bold', ha='center')
    
    # Сохраняем график в байтовый объект
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor())
    buf.seek(0)
    
    # Закрываем фигуру
    plt.close(fig)
    
    return buf