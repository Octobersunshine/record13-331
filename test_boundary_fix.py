import matplotlib
matplotlib.use("Agg")

from rose_chart import (
    plot_rose_chart,
    plot_proportional_rose_chart,
    plot_stacked_rose_chart,
)
import numpy as np


def test_many_categories():
    """测试场景1：大量类别（20个）+ 长标签 + 大数值差距"""
    print("=" * 60)
    print("测试场景1：20个类别 + 长标签 + 数值差距悬殊")
    print("=" * 60)
    categories = [
        "市场营销部门2024年度总销售额",
        "产品研发中心季度预算执行情况",
        "人力资源招聘与培训综合统计",
        "客户服务满意度调查数据分析报告",
        "供应链管理采购成本控制指标",
        "财务部门年度审计工作完成度",
        "信息技术基础设施升级项目",
        "运营管理效率提升专项行动",
        "销售大区北区业绩完成情况",
        "销售大区南区业绩完成情况",
        "销售大区东区业绩完成情况",
        "销售大区西区业绩完成情况",
        "新产品线A市场推广成效",
        "新产品线B市场推广成效",
        "客户关系管理系统实施进度",
        "企业品牌形象建设工程",
        "海外市场开拓战略执行情况",
        "战略合作伙伴关系维护指标",
        "内部流程优化项目里程碑",
        "员工敬业度与企业文化建设",
    ]
    np.random.seed(42)
    values = np.random.lognormal(mean=5.5, sigma=1.4, size=20).astype(int).tolist()
    print(f"  类别数: {len(categories)}")
    print(f"  最大值: {max(values)}, 最小值: {min(values)}, 差距倍数: {max(values)/min(values):.1f}x")

    fig, ax = plot_rose_chart(
        categories=categories,
        values=values,
        title="各部门2024年度综合指标对比（多类别+长标签测试）",
        value_format="{:,.0f}",
        show_value=True,
        show=False,
        save_path="test_many_categories.png",
        figsize=(14, 14),
    )
    print("  ✓ 已保存至 test_many_categories.png")


def test_extreme_values():
    """测试场景2：极端大数值 + 超小数值混合（确保不会溢出）"""
    print("\n" + "=" * 60)
    print("测试场景2：极端大数值混合超小数值")
    print("=" * 60)
    categories = ["A类产品", "B类产品", "C类产品", "D类产品", "E类产品", "F类产品"]
    values = [1_500_000, 980_000, 12_500, 720_000, 3_200, 450_000]
    print(f"  数值范围: {min(values):,} ~ {max(values):,}")
    print(f"  最大/最小比值: {max(values)/min(values):.0f}x")

    fig, ax = plot_rose_chart(
        categories=categories,
        values=values,
        title="各类产品年度营收对比（极值混合测试）",
        value_format="{:,.0f}",
        show_value=True,
        show=False,
        save_path="test_extreme_values.png",
    )
    print("  ✓ 已保存至 test_extreme_values.png")


def test_stacked_many_series():
    """测试场景3：分组玫瑰图 - 多系列 + 多类别 + 长系列名"""
    print("\n" + "=" * 60)
    print("测试场景3：分组玫瑰图 - 6个系列 x 8个类别")
    print("=" * 60)
    categories = ["一季度", "二季度", "三季度", "四季度",
                  "五季度模拟", "六季度模拟", "七季度模拟", "八季度模拟"]
    series_data = {
        "华东区域销售中心第一事业部": [320, 410, 380, 520, 480, 560, 590, 640],
        "华东区域销售中心第二事业部": [280, 320, 350, 410, 390, 450, 480, 510],
        "华南区域销售中心综合事业部": [210, 260, 300, 340, 360, 400, 420, 460],
        "华北区域销售中心重点客户部": [180, 220, 240, 290, 310, 350, 380, 410],
        "华中区域销售中心渠道拓展部": [150, 180, 210, 250, 270, 300, 330, 360],
        "西南西北区域销售联合团队": [120, 140, 160, 190, 210, 240, 260, 290],
    }
    print(f"  系列数: {len(series_data)}, 类别数: {len(categories)}")
    print(f"  系列名最大长度: {max(len(k) for k in series_data.keys())}")

    fig, ax = plot_stacked_rose_chart(
        categories=categories,
        series_data=series_data,
        title="各区域事业部多季度销售趋势对比",
        legend_title="区域事业部",
        figsize=(14, 14),
        show=False,
        save_path="test_stacked_many_series.png",
    )
    print("  ✓ 已保存至 test_stacked_many_series.png")


def test_original_demos():
    """测试场景4：原有示例仍能正常工作（回归测试）"""
    print("\n" + "=" * 60)
    print("测试场景4：回归测试 - 原有示例")
    print("=" * 60)

    categories = ["销售部", "运营部", "技术部", "市场部", "人事部", "财务部", "产品部"]
    values = [120, 85, 200, 65, 45, 55, 90]
    plot_rose_chart(
        categories=categories,
        values=values,
        title="回归测试：部门人员分布",
        value_format="{:.0f}人",
        show=False,
        save_path="regression_basic.png",
    )
    print("  ✓ 基础玫瑰图")

    categories = ["品牌A", "品牌B", "品牌C", "品牌D", "品牌E", "品牌F"]
    values = [350, 280, 200, 150, 120, 100]
    plot_proportional_rose_chart(
        categories=categories,
        values=values,
        title="回归测试：市场份额占比",
        show=False,
        save_path="regression_proportion.png",
    )
    print("  ✓ 比例玫瑰图")

    categories = ["Q1", "Q2", "Q3", "Q4"]
    series_data = {
        "产品线A": [120, 150, 180, 210],
        "产品线B": [90, 110, 130, 160],
        "产品线C": [60, 80, 100, 125],
    }
    plot_stacked_rose_chart(
        categories=categories,
        series_data=series_data,
        title="回归测试：季度销售对比",
        legend_title="产品系列",
        show=False,
        save_path="regression_stacked.png",
    )
    print("  ✓ 分组玫瑰图")


if __name__ == "__main__":
    print("\n" + "🔥" * 30)
    print("南丁格尔玫瑰图 - 边界溢出 Bug 修复验证测试")
    print("🔥" * 30 + "\n")

    test_many_categories()
    test_extreme_values()
    test_stacked_many_series()
    test_original_demos()

    print("\n" + "=" * 60)
    print("✅ 所有测试场景运行完成！")
    print("请查看生成的 7 张 PNG 图片，确认图形均在画布边界内。")
    print("=" * 60)
