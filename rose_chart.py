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
import matplotlib.colors as mcolors
import numpy as np
from typing import List, Optional, Tuple, Union


def _hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        hex_color = "".join(c * 2 for c in hex_color)
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def _rgb_to_hex(rgb: Tuple[float, float, float]) -> str:
    rgb_255 = tuple(max(0, min(255, int(round(c * 255)))) for c in rgb)
    return "#{:02X}{:02X}{:02X}".format(*rgb_255)


def _adjust_brightness(rgb: Tuple[float, float, float], factor: float) -> Tuple[float, float, float]:
    if factor >= 1.0:
        return tuple(c + (1.0 - c) * (factor - 1.0) for c in rgb)
    else:
        return tuple(c * factor for c in rgb)


def _generate_gradient_colors(
    values: List[Union[int, float]],
    use_gradient: bool = False,
    gradient_cmap: str = "YlOrRd",
    gradient_base_color: Optional[str] = None,
    gradient_reverse: bool = False,
) -> List:
    if not use_gradient and gradient_base_color is None:
        return []

    values_arr = np.array(values, dtype=float)
    v_min = np.min(values_arr)
    v_max = np.max(values_arr)
    if v_max - v_min < 1e-9:
        ratios = np.full(len(values_arr), 0.5)
    else:
        ratios = (values_arr - v_min) / (v_max - v_min)

    if gradient_reverse:
        ratios = 1.0 - ratios

    result_colors = []

    if gradient_base_color is not None:
        base_rgb = tuple(c / 255.0 for c in _hex_to_rgb(gradient_base_color))
        for ratio in ratios:
            factor = 0.45 + ratio * 0.50
            adjusted = _adjust_brightness(base_rgb, factor)
            result_colors.append((*adjusted, 1.0))
    else:
        cmap = plt.cm.get_cmap(gradient_cmap)
        for ratio in ratios:
            result_colors.append(cmap(ratio))

    return result_colors


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
    use_gradient: bool = False,
    gradient_cmap: str = "YlOrRd",
    gradient_base_color: Optional[str] = None,
    gradient_reverse: bool = False,
    show_colorbar: bool = False,
    colorbar_label: str = "数值大小",
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
        自定义颜色列表，若为 None 则使用默认配色；与 use_gradient 同时设置时以渐变优先
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
    use_gradient : bool
        是否启用颜色渐变（根据数值大小映射颜色深浅）
    gradient_cmap : str
        渐变使用的 matplotlib colormap 名称，如 'YlOrRd'、'Blues'、'viridis'、'Reds' 等
        仅在 gradient_base_color 为 None 时生效
    gradient_base_color : Optional[str]
        单色渐变基准色（HEX 格式，如 '#3498DB'），设置后将以该色为基础按明度生成渐变
        优先级高于 gradient_cmap
    gradient_reverse : bool
        是否反转渐变方向：False=大值深/暖色，True=大值浅/冷色
    show_colorbar : bool
        是否显示颜色条图例（仅 colormap 渐变模式下效果最佳）
    colorbar_label : str
        颜色条的标题文字

    Returns
    -------
    Tuple[plt.Figure, plt.Axes]
        返回 matplotlib 的 Figure 和 Axes 对象，便于后续自定义调整

    Examples
    --------
    >>> categories = ['销售', '运营', '技术', '市场', '人事', '财务']
    >>> values = [120, 85, 200, 65, 45, 55]
    >>> fig, ax = plot_rose_chart(categories, values, title='部门人员分布')
    >>> # 启用 YlOrRd 橙红色渐变
    >>> fig, ax = plot_rose_chart(categories, values, use_gradient=True, gradient_cmap='YlOrRd')
    >>> # 启用蓝色单色渐变
    >>> fig, ax = plot_rose_chart(categories, values, gradient_base_color='#3498DB')
    """
    if len(categories) != len(values):
        raise ValueError("categories 和 values 的长度必须一致")

    n = len(categories)

    gradient_colors = _generate_gradient_colors(
        values=values,
        use_gradient=use_gradient,
        gradient_cmap=gradient_cmap,
        gradient_base_color=gradient_base_color,
        gradient_reverse=gradient_reverse,
    )

    if len(gradient_colors) > 0:
        colors = gradient_colors
    elif colors is None:
        cmap = plt.cm.get_cmap("Set2", n)
        colors = [cmap(i) for i in range(n)]
    elif len(colors) != n:
        raise ValueError("colors 列表长度需与 categories 一致")

    using_cmap_gradient = len(gradient_colors) > 0 and gradient_base_color is None

    values_arr = np.array(values, dtype=float)
    theta = np.linspace(0.0, 2 * np.pi, n, endpoint=False)
    width = 2 * np.pi / n

    max_val = np.max(values_arr) if len(values_arr) > 0 else 1.0
    if max_val <= 0:
        max_val = 1.0

    max_label_len = max(len(str(c)) for c in categories) if n > 0 else 0
    scale_factor = 1.25
    if show_value:
        scale_factor += 0.08
    if max_label_len >= 6:
        scale_factor += 0.04 * min(max_label_len - 5, 5)
    if n >= 10:
        scale_factor += 0.08
    if n >= 16:
        scale_factor += 0.07
    r_max_limit = max_val * scale_factor

    fig = plt.figure(figsize=figsize)
    fig.patch.set_facecolor("white")
    ax = fig.add_subplot(111, projection="polar")

    margin_factor = 0.18
    if max_label_len >= 8:
        margin_factor += 0.04
    if n >= 12:
        margin_factor += 0.03
    margin_factor = min(margin_factor, 0.32)
    left = right = bottom = top = margin_factor
    fig.subplots_adjust(left=left, right=1 - right, bottom=bottom, top=1 - top)

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

    rticks_count = 5
    rticks_step = r_max_limit / (rticks_count + 1)
    rticks = np.arange(rticks_step, r_max_limit + 1e-9, rticks_step)[:rticks_count]
    ax.set_rlim(0, r_max_limit)
    ax.set_yticks(rticks)
    ax.set_rlabel_position(rlabel_position)
    ax.tick_params(axis="y", labelsize=9, grid_alpha=0.5)

    ax.grid(True, color=grid_color, linestyle="--", linewidth=0.8)
    ax.spines["polar"].set_color(grid_color)
    ax.spines["polar"].set_linewidth(0.8)

    if show_value:
        for bar, angle, val in zip(bars, theta, values_arr):
            if val <= 0:
                continue
            if max_val > 0 and val / max_val < 0.12:
                label_r = val + r_max_limit * 0.06
                text_color = "black"
                bbox_alpha = 0.55
            else:
                label_r = val / 2
                text_color = "white"
                bbox_alpha = 0.4
            label_text = value_format.format(val)
            ax.text(
                angle,
                label_r,
                label_text,
                ha="center",
                va="center",
                fontsize=value_fontsize,
                fontweight="bold",
                color=text_color,
                clip_on=False,
                bbox=dict(
                    boxstyle="round,pad=0.22",
                    facecolor="black",
                    alpha=bbox_alpha,
                    edgecolor="none",
                ),
            )

    ax.set_title(title, fontsize=title_fontsize, fontweight="bold", pad=28)

    if show_colorbar and using_cmap_gradient:
        v_min = float(np.min(values_arr)) if len(values_arr) > 0 else 0.0
        v_max = float(np.max(values_arr)) if len(values_arr) > 0 else 1.0
        if v_max - v_min < 1e-9:
            v_max = v_min + 1.0
        sm = plt.cm.ScalarMappable(
            cmap=plt.cm.get_cmap(gradient_cmap),
            norm=plt.Normalize(vmin=v_min, vmax=v_max),
        )
        sm.set_array([])
        if gradient_reverse:
            sm.norm = plt.Normalize(vmin=v_max, vmax=v_min)
        cbar = fig.colorbar(
            sm,
            ax=ax,
            orientation="vertical",
            pad=0.02,
            fraction=0.045,
            shrink=0.8,
        )
        cbar.set_label(colorbar_label, fontsize=11)
        cbar.ax.tick_params(labelsize=9)

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
    use_series_gradient: bool = False,
    series_gradient_reverse: bool = False,
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
        自定义颜色字典，键为系列名，值为颜色字符串（HEX/RGB）。当 use_series_gradient=True
        时，此颜色将作为各系列的渐变基准色
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
    use_series_gradient : bool
        是否在每个系列内部按数值大小启用明度渐变（大值=深色，小值=浅色）
    series_gradient_reverse : bool
        是否反转系列内渐变方向：False=大值深色，True=大值浅色

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
    >>> # 启用系列内明度渐变（每个产品内部按季度数值深浅变化）
    >>> fig, ax = plot_stacked_rose_chart(categories, series_data, use_series_gradient=True)
    """
    series_names = list(series_data.keys())
    n_series = len(series_names)
    n_categories = len(categories)

    for name, data in series_data.items():
        if len(data) != n_categories:
            raise ValueError(f"系列 '{name}' 的数据长度({len(data)})与 categories 长度({n_categories})不一致")

    if colors is None:
        cmap = plt.cm.get_cmap("tab10", n_series)
        colors = {}
        for i, name in enumerate(series_names):
            rgba = cmap(i)
            colors[name] = _rgb_to_hex((rgba[0], rgba[1], rgba[2]))

    series_base_colors = {}
    for name in series_names:
        c = colors.get(name, "#3498DB")
        if isinstance(c, tuple):
            if len(c) >= 4:
                c = _rgb_to_hex((c[0], c[1], c[2]))
            elif len(c) == 3:
                c = _rgb_to_hex(c)
        series_base_colors[name] = c if isinstance(c, str) else "#3498DB"

    all_values = np.concatenate([np.array(v, dtype=float) for v in series_data.values()])
    max_val = np.max(all_values) if len(all_values) > 0 else 1.0
    if max_val <= 0:
        max_val = 1.0

    max_label_len = max(len(str(c)) for c in categories) if n_categories > 0 else 0
    max_series_name_len = max(len(str(s)) for s in series_names) if n_series > 0 else 0

    scale_factor = 1.28
    scale_factor += 0.02 * min(n_series, 5)
    if max_label_len >= 6:
        scale_factor += 0.035 * min(max_label_len - 5, 5)
    if n_categories >= 8:
        scale_factor += 0.07
    if n_categories >= 12:
        scale_factor += 0.06
    r_max_limit = max_val * scale_factor

    fig = plt.figure(figsize=figsize)
    fig.patch.set_facecolor("white")
    ax = fig.add_subplot(111, projection="polar")

    left_margin = 0.18
    right_margin = 0.22 + 0.025 * min(max_series_name_len, 8)
    bottom_margin = 0.18
    top_margin = 0.20
    if max_label_len >= 8:
        left_margin += 0.04
        bottom_margin += 0.03
    if n_categories >= 10:
        left_margin += 0.02
        bottom_margin += 0.02
    left_margin = min(left_margin, 0.30)
    right_margin = min(right_margin, 0.40)
    bottom_margin = min(bottom_margin, 0.30)
    top_margin = min(top_margin, 0.30)
    fig.subplots_adjust(
        left=left_margin,
        right=1 - right_margin,
        bottom=bottom_margin,
        top=1 - top_margin,
    )

    group_width = 2 * np.pi / n_categories
    bar_width = group_width * 0.85 / n_series
    theta = np.linspace(0.0, 2 * np.pi, n_categories, endpoint=False)

    bars_by_series = {}
    legend_handles = []
    for s_idx, series_name in enumerate(series_names):
        values_arr = np.array(series_data[series_name], dtype=float)
        base_hex = series_base_colors.get(series_name, "#3498DB")

        if use_series_gradient:
            s_max = float(np.max(values_arr)) if len(values_arr) > 0 else 1.0
            s_min = float(np.min(values_arr)) if len(values_arr) > 0 else 0.0
            if s_max - s_min < 1e-9:
                ratios = np.full(len(values_arr), 0.5)
            else:
                ratios = (values_arr - s_min) / (s_max - s_min)
            if series_gradient_reverse:
                ratios = 1.0 - ratios
            base_rgb = tuple(c / 255.0 for c in _hex_to_rgb(base_hex))
            series_colors = []
            for r in ratios:
                factor = 0.45 + r * 0.50
                adj = _adjust_brightness(base_rgb, factor)
                series_colors.append((*adj, 0.88))
        else:
            base_rgb = tuple(c / 255.0 for c in _hex_to_rgb(base_hex))
            series_colors = [(*base_rgb, 0.88) for _ in values_arr]

        if counterclock:
            offset = (-group_width * 0.425) + (s_idx + 0.5) * bar_width
        else:
            offset = (group_width * 0.425) - (s_idx + 0.5) * bar_width

        bars = ax.bar(
            theta + offset,
            values_arr,
            width=bar_width,
            bottom=0,
            color=series_colors,
            edgecolor="white",
            linewidth=1.2,
            align="center",
        )
        bars_by_series[series_name] = bars

        legend_patch = plt.matplotlib.patches.Patch(
            facecolor=(*tuple(c / 255.0 for c in _hex_to_rgb(base_hex)), 0.88),
            edgecolor="white",
            linewidth=1.2,
            label=series_name,
        )
        legend_handles.append(legend_patch)

    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1 if counterclock else 1)
    ax.set_xticks(theta)
    ax.set_xticklabels(categories, fontsize=label_fontsize)

    rticks_count = 5
    rticks_step = r_max_limit / (rticks_count + 1)
    rticks = np.arange(rticks_step, r_max_limit + 1e-9, rticks_step)[:rticks_count]
    ax.set_rlim(0, r_max_limit)
    ax.set_yticks(rticks)
    ax.set_rlabel_position(22.5)
    ax.tick_params(axis="y", labelsize=9, grid_alpha=0.5)

    ax.grid(True, color="#E8E8E8", linestyle="--", linewidth=0.8)
    ax.spines["polar"].set_color("#E8E8E8")

    legend_right_pos = 1.28 + 0.015 * min(max_series_name_len, 10)
    legend = ax.legend(
        handles=legend_handles,
        loc="upper left",
        bbox_to_anchor=(legend_right_pos, 1.06),
        title=legend_title,
        fontsize=10,
        title_fontsize=11,
        frameon=True,
        fancybox=True,
    )
    legend.get_frame().set_alpha(0.92)

    ax.set_title(title, fontsize=title_fontsize, fontweight="bold", pad=26)

    if save_path:
        fig.savefig(save_path, dpi=dpi, bbox_inches="tight", facecolor="white")

    if show:
        plt.show()

    return fig, ax


if __name__ == "__main__":
    pass
