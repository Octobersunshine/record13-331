import matplotlib
from matplotlib import font_manager
import platform
import warnings

system_name = platform.system()
if system_name == "Windows":
    font_candidates = ["Microsoft YaHei", "SimHei", "SimSun", "KaiTi", "Arial Unicode MS"]
elif system_name == "Darwin":
    font_candidates = ["PingFang SC", "Heiti SC", "STHeiti", "Arial Unicode MS"]
else:
    font_candidates = ["Noto Sans CJK SC", "WenQuanYi Zen Hei", "SimHei", "Microsoft YaHei", "Arial Unicode MS"]

available_fonts = set(f.name for f in font_manager.fontManager.ttflist)
selected_font = None
for font in font_candidates:
    if font in available_fonts:
        selected_font = font
        break

if selected_font:
    matplotlib.rcParams["font.sans-serif"] = [selected_font] + matplotlib.rcParams["font.sans-serif"]
else:
    warnings.warn(
        "未找到支持中文的字体，中文标签可能显示为方框。"
        "建议安装 Microsoft YaHei、SimHei 或 Noto Sans CJK 等中文字体。",
        UserWarning,
    )

matplotlib.rcParams["axes.unicode_minus"] = False

import matplotlib.pyplot as plt
import numpy as np
from typing import List, Optional, Tuple, Union


def plot_rose_chart(
    categories: List[str],
    values: List[Union[int, float]],
    title: str = "南丁格尔玫瑰图",
    colors: Optional[List[str]] = None,
    figsize: Tuple[int, int] = (10, 10),
    show_value: bool = True,
    value_format: str = "{:.1f}",
    start_angle: float = 90,
    counterclock: bool = True,
    edgecolor: str = "white",
    linewidth: float = 1.5,
    alpha: float = 0.85,
    label_fontsize: int = 11,
    title_fontsize: int = 18,
    value_fontsize: int = 10,
    rlabel_position: float = 22.5,
    grid_color: str = "#E8E8E8",
    save_path: Optional[str] = None,
    dpi: int = 150,
    show: bool = True,
) -> Tuple[plt.Figure, plt.Axes]:
    """
    绘制南丁格尔玫瑰图（极坐标条形图），用于对比多个类别的数量或比例。

    Parameters
    ----------
    categories : List[str]
        类别名称列表，例如 ['A类', 'B类', 'C类']
    values : List[Union[int, float]]
        对应类别的数值列表，长度需与 categories 一致
    title : str
        图表标题
    colors : Optional[List[str]]
        自定义颜色列表，若为 None 则使用默认渐变色
    figsize : Tuple[int, int]
        图像尺寸 (宽, 高)，单位为英寸
    show_value : bool
        是否在扇形上显示数值标签
    value_format : str
        数值显示格式，如 "{:.0f}" 显示整数，"{:.1%}" 显示百分比
    start_angle : float
        起始角度（度），默认 90 度（正上方）
    counterclock : bool
        是否逆时针排列，True 为逆时针，False 为顺时针
    edgecolor : str
        扇形边框颜色
    linewidth : float
        扇形边框线宽
    alpha : float
        扇形透明度 (0-1)
    label_fontsize : int
        类别标签字号
    title_fontsize : int
        标题字号
    value_fontsize : int
        数值标签字号
    rlabel_position : float
        径向刻度标签的角度位置
    grid_color : str
        网格线颜色
    save_path : Optional[str]
        图片保存路径，若为 None 则不保存
    dpi : int
        保存图片的分辨率
    show : bool
        是否调用 plt.show() 显示图像

    Returns
    -------
    Tuple[plt.Figure, plt.Axes]
        返回 matplotlib 的 Figure 和 Axes 对象，便于后续自定义调整

    Examples
    --------
    >>> categories = ['销售', '运营', '技术', '市场', '人事', '财务']
    >>> values = [120, 85, 200, 65, 45, 55]
    >>> fig, ax = plot_rose_chart(categories, values, title='部门人员分布')
    """
    if len(categories) != len(values):
        raise ValueError("categories 和 values 的长度必须一致")

    n = len(categories)

    if colors is None:
        cmap = plt.cm.get_cmap("Set2", n)
        colors = [cmap(i) for i in range(n)]
    elif len(colors) != n:
        raise ValueError("colors 列表长度需与 categories 一致")

    values_arr = np.array(values, dtype=float)
    theta = np.linspace(0.0, 2 * np.pi, n, endpoint=False)
    width = 2 * np.pi / n

    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection="polar")

    bars = ax.bar(
        theta,
        values_arr,
        width=width,
        bottom=0.0,
        color=colors,
        edgecolor=edgecolor,
        linewidth=linewidth,
        alpha=alpha,
        align="center",
    )

    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1 if counterclock else 1)
    theta_offset = np.deg2rad(start_angle - 90)
    if counterclock:
        ax.set_theta_offset(theta_offset)
    else:
        ax.set_theta_offset(-theta_offset)

    ax.set_xticks(theta)
    ax.set_xticklabels(categories, fontsize=label_fontsize)

    max_val = np.max(values_arr) if len(values_arr) > 0 else 1
    rticks_count = 5
    rticks = np.linspace(0, max_val, rticks_count + 1)[1:]
    ax.set_rlim(0, max_val * 1.15)
    ax.set_yticks(rticks)
    ax.set_rlabel_position(rlabel_position)
    ax.tick_params(axis="y", labelsize=9, grid_alpha=0.5)

    ax.grid(True, color=grid_color, linestyle="--", linewidth=0.8)
    ax.spines["polar"].set_color(grid_color)
    ax.spines["polar"].set_linewidth(0.8)

    if show_value:
        for bar, angle, val in zip(bars, theta, values_arr):
            mid_r = val / 2
            label_text = value_format.format(val)
            ax.text(
                angle,
                mid_r,
                label_text,
                ha="center",
                va="center",
                fontsize=value_fontsize,
                fontweight="bold",
                color="white",
                bbox=dict(
                    boxstyle="round,pad=0.2",
                    facecolor="black",
                    alpha=0.4,
                    edgecolor="none",
                ),
            )

    ax.set_title(title, fontsize=title_fontsize, fontweight="bold", pad=30)

    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=dpi, bbox_inches="tight", facecolor="white")

    if show:
        plt.show()

    return fig, ax


def plot_proportional_rose_chart(
    categories: List[str],
    values: List[Union[int, float]],
    title: str = "南丁格尔玫瑰图（比例）",
    **kwargs,
) -> Tuple[plt.Figure, plt.Axes]:
    """
    绘制显示比例的南丁格尔玫瑰图，数值自动转换为百分比。

    Parameters
    ----------
    categories : List[str]
        类别名称列表
    values : List[Union[int, float]]
        对应类别的数值列表
    title : str
        图表标题
    **kwargs
        其他传递给 plot_rose_chart 的参数

    Returns
    -------
    Tuple[plt.Figure, plt.Axes]

    Examples
    --------
    >>> categories = ['A', 'B', 'C', 'D', 'E']
    >>> values = [30, 50, 20, 80, 40]
    >>> fig, ax = plot_proportional_rose_chart(categories, values)
    """
    total = sum(values)
    if total == 0:
        raise ValueError("values 的总和不能为 0")
    proportions = [v / total * 100 for v in values]
    kwargs.setdefault("value_format", "{:.1f}%")
    return plot_rose_chart(categories, proportions, title=title, **kwargs)


def plot_stacked_rose_chart(
    categories: List[str],
    series_data: dict,
    title: str = "分组南丁格尔玫瑰图",
    colors: Optional[dict] = None,
    figsize: Tuple[int, int] = (12, 12),
    legend_title: str = "",
    value_format: str = "{:.0f}",
    label_fontsize: int = 11,
    title_fontsize: int = 18,
    save_path: Optional[str] = None,
    dpi: int = 150,
    show: bool = True,
    counterclock: bool = True,
) -> Tuple[plt.Figure, plt.Axes]:
    """
    绘制分组（多系列）南丁格尔玫瑰图，用于多维度对比。

    Parameters
    ----------
    categories : List[str]
        类别名称列表（角度方向）
    series_data : dict
        系列数据字典，键为系列名，值为与 categories 等长的数值列表
        例如: {'2023年': [10, 20, 30], '2024年': [15, 25, 35]}
    title : str
        图表标题
    colors : Optional[dict]
        自定义颜色字典，键为系列名，值为颜色字符串
    figsize : Tuple[int, int]
        图像尺寸
    legend_title : str
        图例标题
    value_format : str
        数值显示格式
    label_fontsize : int
        类别标签字号
    title_fontsize : int
        标题字号
    save_path : Optional[str]
        保存路径
    dpi : int
        图片分辨率
    show : bool
        是否显示图片
    counterclock : bool
        是否逆时针排列

    Returns
    -------
    Tuple[plt.Figure, plt.Axes]

    Examples
    --------
    >>> categories = ['Q1', 'Q2', 'Q3', 'Q4']
    >>> series_data = {
    ...     '产品A': [120, 150, 180, 200],
    ...     '产品B': [80, 100, 90, 130],
    ... }
    >>> fig, ax = plot_stacked_rose_chart(categories, series_data)
    """
    series_names = list(series_data.keys())
    n_series = len(series_names)
    n_categories = len(categories)

    for name, data in series_data.items():
        if len(data) != n_categories:
            raise ValueError(f"系列 '{name}' 的数据长度({len(data)})与 categories 长度({n_categories})不一致")

    if colors is None:
        cmap = plt.cm.get_cmap("tab10", n_series)
        colors = {series_names[i]: cmap(i) for i in range(n_series)}

    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection="polar")

    group_width = 2 * np.pi / n_categories
    bar_width = group_width * 0.85 / n_series
    theta = np.linspace(0.0, 2 * np.pi, n_categories, endpoint=False)

    bars_by_series = {}
    for s_idx, series_name in enumerate(series_names):
        values_arr = np.array(series_data[series_name], dtype=float)
        if counterclock:
            offset = (-group_width * 0.425) + (s_idx + 0.5) * bar_width
        else:
            offset = (group_width * 0.425) - (s_idx + 0.5) * bar_width
        bars = ax.bar(
            theta + offset,
            values_arr,
            width=bar_width,
            bottom=0,
            color=colors.get(series_name, f"C{s_idx}"),
            edgecolor="white",
            linewidth=1.2,
            alpha=0.88,
            label=series_name,
            align="center",
        )
        bars_by_series[series_name] = bars

    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1 if counterclock else 1)
    ax.set_xticks(theta)
    ax.set_xticklabels(categories, fontsize=label_fontsize)

    all_values = np.concatenate([np.array(v) for v in series_data.values()])
    max_val = np.max(all_values) if len(all_values) > 0 else 1
    rticks = np.linspace(0, max_val, 6)[1:]
    ax.set_rlim(0, max_val * 1.2)
    ax.set_yticks(rticks)
    ax.set_rlabel_position(22.5)
    ax.tick_params(axis="y", labelsize=9, grid_alpha=0.5)

    ax.grid(True, color="#E8E8E8", linestyle="--", linewidth=0.8)
    ax.spines["polar"].set_color("#E8E8E8")

    legend = ax.legend(
        loc="upper right",
        bbox_to_anchor=(1.35, 1.1),
        title=legend_title,
        fontsize=10,
        title_fontsize=11,
        frameon=True,
        fancybox=True,
    )
    legend.get_frame().set_alpha(0.9)

    ax.set_title(title, fontsize=title_fontsize, fontweight="bold", pad=30)
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=dpi, bbox_inches="tight", facecolor="white")

    if show:
        plt.show()

    return fig, ax


if __name__ == "__main__":
    pass
