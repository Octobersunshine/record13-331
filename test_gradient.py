import matplotlib
matplotlib.use("Agg")

from rose_chart import (
    plot_rose_chart,
    plot_proportional_rose_chart,
    plot_stacked_rose_chart,
)


def test_cmap_gradient():
    """测试1：使用 matplotlib colormap 渐变 (YlOrRd) + 颜色条"""
    print("=" * 60)
    print("测试1：Colormap 渐变 (YlOrRd 橙红) + 颜色条")
    print("=" * 60)
    categories = ["北京", "上海", "广州", "深圳", "杭州", "成都", "武汉", "南京"]
    values = [41610, 47218, 30355, 34606, 20059, 22074, 19569, 17421]
    fig, ax = plot_rose_chart(
        categories=categories,
        values=values,
        title="2024年主要城市GDP对比（YlOrRd 渐变）",
        use_gradient=True,
        gradient_cmap="YlOrRd",
        show_colorbar=True,
        colorbar_label="GDP（亿元）",
        value_format="{:,.0f}",
        show=False,
        save_path="grad_cmap_ylorrd.png",
    )
    print("  ✓ 已保存 grad_cmap_ylorrd.png")


def test_cmap_viridis():
    """测试2：使用 viridis 渐变色（感知均匀）"""
    print("\n" + "=" * 60)
    print("测试2：Viridis 渐变 + 反转（大值=浅色）")
    print("=" * 60)
    categories = ["A类", "B类", "C类", "D类", "E类", "F类", "G类"]
    values = [120, 85, 200, 65, 45, 55, 110]
    fig, ax = plot_rose_chart(
        categories=categories,
        values=values,
        title="各类别数量对比（Viridis 反转渐变）",
        use_gradient=True,
        gradient_cmap="viridis",
        gradient_reverse=True,
        show_colorbar=True,
        show=False,
        save_path="grad_cmap_viridis.png",
    )
    print("  ✓ 已保存 grad_cmap_viridis.png")


def test_mono_blue_gradient():
    """测试3：单色明度渐变（蓝色基准）"""
    print("\n" + "=" * 60)
    print("测试3：单色明度渐变（#3498DB 蓝色）")
    print("=" * 60)
    categories = ["销售", "运营", "技术", "市场", "人事", "财务", "产品", "行政"]
    values = [120, 85, 200, 65, 45, 55, 90, 40]
    fig, ax = plot_rose_chart(
        categories=categories,
        values=values,
        title="各部门人员分布（蓝色单色渐变）",
        gradient_base_color="#3498DB",
        value_format="{:.0f}人",
        show=False,
        save_path="grad_mono_blue.png",
    )
    print("  ✓ 已保存 grad_mono_blue.png")


def test_mono_red_gradient_reverse():
    """测试4：单色渐变（红色基准）+ 反转"""
    print("\n" + "=" * 60)
    print("测试4：单色渐变（#E74C3C 红色）+ 反转（大值=浅色）")
    print("=" * 60)
    categories = ["一月", "二月", "三月", "四月", "五月", "六月",
                  "七月", "八月", "九月", "十月", "十一月", "十二月"]
    values = [180, 120, 220, 260, 310, 380, 420, 400, 350, 280, 230, 190]
    fig, ax = plot_rose_chart(
        categories=categories,
        values=values,
        title="2024年月度销售趋势（红色反转渐变）",
        gradient_base_color="#E74C3C",
        gradient_reverse=True,
        value_format="{:.0f}",
        show=False,
        save_path="grad_mono_red_reverse.png",
    )
    print("  ✓ 已保存 grad_mono_red_reverse.png")


def test_proportion_gradient():
    """测试5：比例玫瑰图 + 渐变"""
    print("\n" + "=" * 60)
    print("测试5：比例玫瑰图 + Greens 绿色渐变")
    print("=" * 60)
    categories = ["Chrome", "Safari", "Edge", "Firefox", "Opera", "其他"]
    values = [65.2, 18.5, 5.3, 3.1, 2.4, 5.5]
    fig, ax = plot_proportional_rose_chart(
        categories=categories,
        values=values,
        title="全球浏览器市场份额（Greens 渐变）",
        use_gradient=True,
        gradient_cmap="Greens",
        show_colorbar=True,
        colorbar_label="市场份额（%）",
        show=False,
        save_path="grad_proportion_greens.png",
    )
    print("  ✓ 已保存 grad_proportion_greens.png")


def test_stacked_series_gradient():
    """测试6：分组玫瑰图 + 系列内明度渐变"""
    print("\n" + "=" * 60)
    print("测试6：分组玫瑰图 + 系列内明度渐变")
    print("=" * 60)
    categories = ["Q1", "Q2", "Q3", "Q4"]
    series_data = {
        "产品线A": [120, 150, 180, 210],
        "产品线B": [80, 110, 130, 160],
        "产品线C": [60, 80, 100, 125],
        "产品线D": [40, 55, 70, 95],
    }
    colors = {
        "产品线A": "#3498DB",
        "产品线B": "#E74C3C",
        "产品线C": "#2ECC71",
        "产品线D": "#F39C12",
    }
    fig, ax = plot_stacked_rose_chart(
        categories=categories,
        series_data=series_data,
        colors=colors,
        title="2024年各产品线季度销售对比（系列内渐变）",
        legend_title="产品系列",
        use_series_gradient=True,
        show=False,
        save_path="grad_stacked_series.png",
        figsize=(13, 13),
    )
    print("  ✓ 已保存 grad_stacked_series.png")


def test_stacked_gradient_custom():
    """测试7：分组玫瑰图 + 多类别 + 系列渐变"""
    print("\n" + "=" * 60)
    print("测试7：分组玫瑰图（6系列 x 8类别）+ 系列内渐变")
    print("=" * 60)
    categories = ["华东", "华南", "华北", "华中", "西南", "西北", "东北", "海外"]
    series_data = {
        "2019年": [320, 280, 260, 190, 150, 120, 160, 90],
        "2020年": [340, 300, 275, 205, 165, 135, 170, 100],
        "2021年": [390, 350, 310, 240, 190, 155, 195, 130],
        "2022年": [450, 410, 370, 290, 230, 190, 230, 165],
        "2023年": [520, 475, 430, 340, 275, 225, 275, 205],
        "2024年": [610, 560, 510, 405, 330, 275, 330, 255],
    }
    colors = {
        "2019年": "#95A5A6",
        "2020年": "#3498DB",
        "2021年": "#2ECC71",
        "2022年": "#F1C40F",
        "2023年": "#E67E22",
        "2024年": "#E74C3C",
    }
    fig, ax = plot_stacked_rose_chart(
        categories=categories,
        series_data=series_data,
        colors=colors,
        title="2019-2024年各区域销售额年度对比（系列内渐变）",
        legend_title="年度",
        use_series_gradient=True,
        show=False,
        save_path="grad_stacked_multi.png",
        figsize=(14, 14),
    )
    print("  ✓ 已保存 grad_stacked_multi.png")


if __name__ == "__main__":
    print("\n🎨" * 30)
    print("南丁格尔玫瑰图 - 颜色渐变功能测试")
    print("🎨" * 30 + "\n")

    test_cmap_gradient()
    test_cmap_viridis()
    test_mono_blue_gradient()
    test_mono_red_gradient_reverse()
    test_proportion_gradient()
    test_stacked_series_gradient()
    test_stacked_gradient_custom()

    print("\n" + "=" * 60)
    print("✅ 全部 7 个渐变测试场景完成！请查看生成的 PNG 图片。")
    print("=" * 60)
