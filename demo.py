import matplotlib
matplotlib.use("Agg")

from rose_chart import (
    plot_rose_chart,
    plot_proportional_rose_chart,
    plot_stacked_rose_chart,
)


def demo_basic_rose():
    """示例1：基础南丁格尔玫瑰图 - 部门人员分布"""
    print("运行示例1：基础玫瑰图（部门人员分布）...")
    categories = ["销售部", "运营部", "技术部", "市场部", "人事部", "财务部", "产品部"]
    values = [120, 85, 200, 65, 45, 55, 90]
    colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", "#DDA0DD", "#FF8C42"]
    fig, ax = plot_rose_chart(
        categories=categories,
        values=values,
        title="公司各部门人员数量分布",
        colors=colors,
        value_format="{:.0f}人",
        show_value=True,
        show=False,
        save_path="output_basic.png",
    )
    print(f"  已保存至 output_basic.png")
    return fig, ax


def demo_proportional_rose():
    """示例2：比例南丁格尔玫瑰图 - 市场份额"""
    print("运行示例2：比例玫瑰图（市场份额）...")
    categories = ["品牌A", "品牌B", "品牌C", "品牌D", "品牌E", "品牌F"]
    values = [350, 280, 200, 150, 120, 100]
    fig, ax = plot_proportional_rose_chart(
        categories=categories,
        values=values,
        title="各品牌市场份额占比",
        value_format="{:.1f}%",
        show=False,
        save_path="output_proportion.png",
    )
    print(f"  已保存至 output_proportion.png")
    return fig, ax


def demo_stacked_rose():
    """示例3：分组南丁格尔玫瑰图 - 季度销售对比"""
    print("运行示例3：分组玫瑰图（季度销售对比）...")
    categories = ["Q1", "Q2", "Q3", "Q4"]
    series_data = {
        "产品线A": [120, 150, 180, 210],
        "产品线B": [90, 110, 130, 160],
        "产品线C": [60, 80, 100, 125],
    }
    colors = {
        "产品线A": "#3498DB",
        "产品线B": "#E74C3C",
        "产品线C": "#2ECC71",
    }
    fig, ax = plot_stacked_rose_chart(
        categories=categories,
        series_data=series_data,
        colors=colors,
        title="2024年各产品线季度销售额对比（万元）",
        legend_title="产品系列",
        show=False,
        save_path="output_stacked.png",
    )
    print(f"  已保存至 output_stacked.png")
    return fig, ax


def demo_customized():
    """示例4：高度自定义玫瑰图"""
    print("运行示例4：自定义玫瑰图（城市GDP）...")
    categories = ["北京", "上海", "广州", "深圳", "杭州", "成都", "武汉", "南京"]
    values = [41610, 47218, 30355, 34606, 20059, 22074, 19569, 17421]
    colors = [
        "#E63946", "#F1A208", "#F4A261", "#2A9D8F",
        "#264653", "#457B9D", "#1D3557", "#606C38",
    ]
    fig, ax = plot_rose_chart(
        categories=categories,
        values=values,
        title="2024年主要城市GDP对比（亿元）",
        colors=colors,
        figsize=(12, 12),
        value_format="{:,.0f}",
        start_angle=90,
        counterclock=False,
        label_fontsize=12,
        title_fontsize=20,
        value_fontsize=9,
        alpha=0.9,
        show=False,
        save_path="output_custom.png",
    )
    print(f"  已保存至 output_custom.png")
    return fig, ax


if __name__ == "__main__":
    print("=" * 60)
    print("南丁格尔玫瑰图 - 示例演示")
    print("=" * 60)

    demo_basic_rose()
    demo_proportional_rose()
    demo_stacked_rose()
    demo_customized()

    print("\n" + "=" * 60)
    print("所有示例运行完成！请查看生成的 PNG 文件。")
    print("=" * 60)
