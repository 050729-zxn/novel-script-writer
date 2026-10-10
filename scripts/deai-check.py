#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""deai-check.py — 去 AI 味检测报告

用法:
  python deai-check.py 文件.txt [--lang zh]
  cat 文件.txt | python deai-check.py - --lang zh

检测: 句法统计(句长分布/节奏)、AI 高频词、万能动作/陈词意象、
结构 tells(否定式平行 / 三段式 / 破折号密度)。
报告只标「候选点」, 由你判断哪些真该删——自然段落别动, 可读性优先。
"""

import argparse
import re
import sys

TELLS = {
    'zh': {
        'filler': ['仿佛', '似乎', '不禁', '不由得', '殊不知', '值得注意的是', '总而言之', '综上所述',
                   '然而', '因此', '进而', '与此同时', '说白了', '可以说', '某种程度上',
                   '他不知道的是', '她不知道的是', '谁也不知道的是'],
        'gesture': ['深吸一口气', '嘴角上扬', '眼中闪过一丝', '心头一震', '微微一笑', '缓缓',
                    '深深', '静静', '轻轻', '夕阳西下', '心如刀割', '不由自主', '暗暗',
                    '命运的齿轮', '命运露出獠牙', '无与伦比', '美轮美奂', '叹为观止', '淋漓尽致',
                    '得天独厚', '独一无二', '前所未有', '不可磨灭', '带着一丝苦笑', '带着三分'],
        'negative_parallel': [r'不是.{1,30}而是', r'不仅.{1,30}更是', r'不只是.{1,30}更是',
                              r'与其说.{1,30}不如说'],
        'triad': [r'第一.{0,40}第二.{0,40}第三', r'首先.{0,40}其次.{0,40}最后'],
    },
    'en': {
        'filler': ['However', 'Moreover', 'Furthermore', 'Additionally', 'In conclusion', 'Ultimately',
                   'delve', 'crucial', 'pivotal', 'robust', 'leverage', 'tapestry', 'nuanced',
                   'multifaceted', 'underscore', 'testament', 'landscape', 'intricate', 'breathtaking',
                   'stunning', 'nestled', 'importantly', 'Indeed',
                   'very', 'really', 'quite', 'somewhat', 'basically', 'actually', 'literally',
                   'clearly', 'obviously', 'simply', 'certainly'],
        'gesture': [],
        'negative_parallel': [r'\bnot\b.{1,40}\bbut\b', r'\bNot just\b.{1,40}\bbut\b',
                              r'\brather than\b'],
        'triad': [r'\bFirst\b.{0,60}\bSecond\b.{0,60}\b(?:Finally|Third)\b',
                  r'\bFirstly\b.{0,60}\bSecondly\b.{0,60}\b(?:Lastly|Thirdly)\b'],
    },
    'fr': {
        'filler': ['En effet', 'Par ailleurs', 'De plus', 'En outre', 'En conclusion',
                   'Il est important de noter', 'crucial', 'essentiel', 'incontournable', 'nuancer'],
        'gesture': [], 'negative_parallel': [], 'triad': [],
    },
    'es': {
        'filler': ['Además', 'Sin embargo', 'Por otro lado', 'En primer lugar', 'Cabe destacar',
                   'En conclusión', 'crucial', 'fundamental', 'multifacético', 'aprovechar'],
        'gesture': [], 'negative_parallel': [], 'triad': [],
    },
    'de': {
        'filler': ['Darüber hinaus', 'Zudem', 'Allerdings', 'Einerseits', 'Andererseits',
                   'Es ist wichtig zu beachten', 'Zusammenfassend'],
        'gesture': [], 'negative_parallel': [], 'triad': [],
    },
    'ja': {
        'filler': ['そして', 'しかし', 'また', '一方で', 'つまり', '要するに'],
        'gesture': [], 'negative_parallel': [], 'triad': [],
    },
}


def read_text(path):
    if path == '-':
        data = sys.stdin.buffer.read()
        return data.decode('utf-8', 'replace')
    with open(path, 'rb') as f:
        return f.read().decode('utf-8', 'replace')


def split_sentences(text, lang):
    if lang in ('zh', 'ja'):
        parts = re.split(r'[。！？!?；;\n]+', text)
    else:
        parts = re.split(r'(?<=[.!?])\s+|\n+', text)
    return [p.strip() for p in parts if p.strip()]


def count_units(text, lang):
    if lang in ('zh', 'ja'):
        return len(re.sub(r'\s', '', text))
    return len(text.split())


def main():
    ap = argparse.ArgumentParser(description='去 AI 味检测报告')
    ap.add_argument('file', help='文本文件路径, "-" 表示从 stdin 读')
    ap.add_argument('--lang', default='zh', help='语言: zh/en/fr/es/de/ja')
    args = ap.parse_args()

    text = read_text(args.file)
    tells = TELLS.get(args.lang, TELLS['zh'])
    lines = text.split('\n')

    sents = split_sentences(text, args.lang)
    n_sents = len(sents)
    n_units = count_units(text, args.lang)
    lens = [len(s.split()) if args.lang not in ('zh', 'ja') else len(s) for s in sents]
    avg = sum(lens) / n_sents if n_sents else 0
    sd = (sum((l - avg) ** 2 for l in lens) / n_sents) ** 0.5 if n_sents else 0

    def scan(patterns, regex=False):
        hits = []
        for pat in patterns:
            if regex:
                for i, ln in enumerate(lines, 1):
                    for _ in re.finditer(pat, ln):
                        hits.append((pat, i, ln.strip()[:64]))
            else:
                for i, ln in enumerate(lines, 1):
                    if pat in ln:
                        hits.append((pat, i, ln.strip()[:64]))
        return hits

    if args.lang in ('zh', 'ja'):
        filler = scan(tells['filler'])
    else:
        filler = scan([r'\b' + re.escape(p) + r'\b' for p in tells['filler']], regex=True)
    gesture = scan(tells['gesture'])
    negpar = scan(tells['negative_parallel'], regex=True)
    triad = scan(tells['triad'], regex=True)

    ndash = text.count('—') + text.count('--')
    dash_per_1k = ndash / (n_units / 1000) if n_units else 0

    buckets = {'极短(<8)': 0, '短(8-15)': 0, '中(16-30)': 0, '长(31-60)': 0, '超长(>60)': 0}
    for l in lens:
        if l < 8:
            buckets['极短(<8)'] += 1
        elif l <= 15:
            buckets['短(8-15)'] += 1
        elif l <= 30:
            buckets['中(16-30)'] += 1
        elif l <= 60:
            buckets['长(31-60)'] += 1
        else:
            buckets['超长(>60)'] += 1

    out = []
    out.append('=== deai-check 报告 (lang=%s) ===' % args.lang)
    out.append('总字数 %d · 句数 %d · 平均句长 %.1f · 句长标准差 %.1f' % (n_units, n_sents, avg, sd))
    out.append('')
    out.append('--- 句长分布 ---')
    out.append('  ' + '  '.join('%s:%d' % (k, v) for k, v in buckets.items()))
    out.append('  (节奏单一信号: 中/长句占绝对多数, 或极短句过密)')
    out.append('')
    out.append('--- AI 高频词/填充词 (%d 处) ---' % len(filler))
    for pat, i, s in filler:
        out.append('  L%d  [%s]  %s' % (i, pat, s))
    out.append('')
    out.append('--- 万能动作/陈词意象 (%d 处) ---' % len(gesture))
    for pat, i, s in gesture:
        out.append('  L%d  [%s]  %s' % (i, pat, s))
    out.append('')
    out.append('--- 结构 tells: 否定式平行 (%d 处) ---' % len(negpar))
    for pat, i, s in negpar:
        out.append('  L%d  [%s]  %s' % (i, pat, s))
    out.append('')
    out.append('--- 结构 tells: 三段式排比(成组出现) (%d 处) ---' % len(triad))
    for pat, i, s in triad:
        out.append('  L%d  [%s]  %s' % (i, pat, s))
    out.append('')
    out.append('--- 破折号密度 ---')
    out.append('  %d 处, 每千字 %.1f (英文 >3/千字 即偏高, 中文应接近 0)' % (ndash, dash_per_1k))
    out.append('')
    out.append('提示: 以上是「候选点」, 由你判断哪些真该删; 自然段落别动, 可读性优先。')

    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    print('\n'.join(out))


if __name__ == '__main__':
    main()
