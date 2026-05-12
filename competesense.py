import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="ReviewSense Agent",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 ReviewSense Agent")
st.subheader("AI 用户评论分析 Agent")

st.write(
    "粘贴用户评论，Agent 会自动分析用户情绪、痛点、需求，并生成产品机会报告。"
)

api_key = st.text_input("请输入你的 OpenAI API Key", type="password")

client = None
if api_key:
    client = OpenAI(api_key=api_key.strip())

st.divider()

product_name = st.text_input(
    "产品名称",
    placeholder="例如：豆包、Kimi、DeepSeek、ChatGPT、DreamCard AI"
)

product_category = st.text_input(
    "产品类型 / 赛道",
    placeholder="例如：AI 聊天助手、AI 搜索、AI 陪伴、电商导购、AIGC 工具"
)

reviews = st.text_area(
    "用户评论",
    height=300,
    placeholder="""请粘贴用户评论，每条评论一行，例如：

回答速度很快，但是有时候理解我的问题不准确。
界面很清爽，比其他 AI 产品更容易上手。
会员价格有点贵，如果只是轻度使用不太划算。
希望可以有长期记忆，不然每次都要重新解释背景。
语音功能不错，但是偶尔会识别错误。"""
)

analysis_focus = st.selectbox(
    "分析重点",
    [
        "整体用户反馈分析",
        "用户痛点分析",
        "产品机会点分析",
        "付费意愿分析",
        "用户体验优化分析"
    ]
)


def run_review_agent():
    prompt = f"""
你是一名资深 AI 产品经理，也是一名专业的用户评论分析 Agent。

你的任务是根据用户输入的产品信息和用户评论，生成一份结构化、专业、可落地的中文用户评论分析报告。

【产品名称】
{product_name}

【产品类型 / 赛道】
{product_category}

【分析重点】
{analysis_focus}

【用户评论】
{reviews}

请按照以下结构输出报告：

## 1. 执行摘要
用 3-5 句话总结用户对该产品的整体态度、主要满意点、主要不满点和潜在机会。

## 2. 用户情绪分析
请将评论中的情绪分为：
- 正面反馈
- 负面反馈
- 中性反馈

并说明每类反馈的典型原因。

## 3. 高频用户痛点
请提取用户评论中反复出现的痛点，并按照以下类别整理：
- 功能问题
- 使用体验问题
- 性能 / 稳定性问题
- 价格 / 付费问题
- 内容质量 / AI 回答质量问题
- 其他问题

每个痛点都要说明：
- 痛点是什么
- 用户为什么在意
- 对产品留存或付费可能产生什么影响

## 4. 用户需求聚类
请将用户评论背后的需求归纳成 4-6 个需求类别。

建议用表格输出：
| 需求类别 | 用户真实需求 | 代表性评论含义 | 产品启示 |

## 5. 用户满意点
总结用户已经认可的产品优势，例如：
- 哪些功能被喜欢
- 哪些体验被认可
- 哪些地方形成了差异化优势

## 6. 产品机会点
基于评论，提出 5 个具体产品机会点。

每个机会点包含：
- 机会点名称
- 对应用户痛点
- 建议功能 / 方案
- 优先级：高 / 中 / 低
- 为什么值得做

## 7. 付费意愿分析
分析哪些评论暗示用户可能愿意付费，哪些因素会降低付费意愿。

请重点分析：
- 用户愿意为什么价值付费
- 用户对价格敏感的原因
- 是否适合设计会员功能
- 哪些功能可以作为付费点

## 8. 产品策略建议
请从以下角度提出建议：
- AI 能力优化
- 用户体验优化
- 差异化定位
- 留存提升
- 商业化设计

## 9. 下一步行动计划
给出一个 MVP 优化计划，包括：
- 立刻应该验证的 3 个问题
- 下一版最应该做的 3 个功能
- 应该继续收集哪些用户数据
- 如何判断这个产品方向是否值得继续投入

要求：
- 使用专业、清晰的中文。
- 不要写空泛套话。
- 每条建议都要尽量具体。
- 重点关注 AI 产品、用户体验、用户需求和商业价值。
- 输出格式清晰，适合直接复制到报告、简历或项目展示中。
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "你是一名专业的 AI 产品经理和用户研究专家，擅长从用户评论中提取痛点、需求、产品机会和商业化策略。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7
    )

    return response.choices[0].message.content


if st.button("生成用户评论分析报告"):
    if not api_key:
        st.error("请先输入 OpenAI API Key。")
    elif not product_name or not product_category or not reviews:
        st.error("请填写产品名称、产品类型和用户评论。")
    else:
        with st.spinner("ReviewSense Agent 正在分析用户评论..."):
            try:
                report = run_review_agent()
                st.success("报告生成成功！")
                st.markdown(report)

                st.download_button(
                    label="下载 Markdown 报告",
                    data=report,
                    file_name=f"{product_name}_review_analysis_report.md",
                    mime="text/markdown"
                )

            except Exception as e:
                st.error("生成失败，请检查 API Key、网络连接或模型权限。")
                st.exception(e)