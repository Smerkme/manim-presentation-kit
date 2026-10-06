from pathlib import Path
import json, os, sys
ROOT=Path(__file__).parent
os.environ['DECK_DIR']=str(ROOT)
REPO = ROOT.parents[1]
sys.path.insert(0,str(REPO))
import manimpango
manimpango.register_font(str(REPO/"assets"/"Inter.ttf"))
manimpango.register_font(str(REPO/"assets"/"JetBrainsMono.ttf"))
from manim import *
from deckkit.base import DeckScene
from deckkit.tokens import *
from deckkit.components import caption, chip, cell, node, mono, sans, rect, b_indicate, b_wave, b_flash_group, b_box

def label(s,x,y,c=INK,size=28): return mono(s,size,c).move_to(pos(x,y))
def path(x1,y1,x2,y2,c=DIM):return Line(pos(x1,y1),pos(x2,y2),color=c,stroke_width=2)
def card(s,x,y,c=ID):return chip(s,c,28,pad=(18,27),stroke=2).move_to(pos(x,y))
class ReactiveFeed(DeckScene):
    def finish(self,*beats):
        for beat in beats:
            beat = beat() if callable(beat) else beat
            if self.left()>beat.run_time+1.5:self.play(beat)
        if self.left()>0:self.wait(self.left())
        # save an independent final frame for review
        self.renderer.update_frame(self)
        self.renderer.get_frame()
        from PIL import Image
        Image.fromarray(self.renderer.get_frame()).save(ROOT/'build'/f'slide-{self._frames_opened}.png')
    def construct(self):
        self.frame('1')
        self.cap=caption('Реактивная лента','Свежая реакция входит в контекст следующего запроса')
        self.a=card('пост A',960,580)
        self.play(FadeIn(self.cap),Create(self.a.box),run_time=1)
        self.play(Write(self.a.label),run_time=.8)
        # Leave the central slot in the lower row for post A.
        grid=VGroup(*[rect(90,120,DIM,2).move_to(pos(420+180*(j%7),400+180*(j//7)))
                     for j in range(14) if j != 10])
        self.play(self.a.animate.move_to(pos(960,580)),LaggedStart(*[FadeIn(o) for o in grid],lag_ratio=.04),run_time=1.3)
        # A reaction appears on the same post, followed by its request path.
        reaction=label('реакция',960,710,ID)
        self.play(FadeIn(reaction),Indicate(self.a,color=ID,scale_factor=1.12),run_time=1)
        target=card('контекст запроса',1410,580,DEC)
        rail=path(670,580,1190,580,MUTED)
        # Clear the path before moving A; draw the connector only after arrival.
        self.play(FadeOut(grid),run_time=.4)
        self.play(self.a.animate.move_to(pos(510,580)),reaction.animate.move_to(pos(510,710)),run_time=.8)
        self.play(Create(rail),FadeIn(target),run_time=.3)
        moving=node(ID,18).move_to(pos(670,580));self.play(MoveAlongPath(moving,rail),run_time=1.2);self.remove(moving)
        payload=label('ID  ·  тип  ·  время',1410,710,MUTED)
        self.play(FadeIn(payload),run_time=.7)
        self.finish(b_flash_group(VGroup(rail),ID,rt=1.2),b_box(target,DEC,rt=1.2))

        self.frame('2')
        cap=caption('Отбор событий в Gateway','Возраст, тип события и время просмотра определяют набор якорей')
        self.play(Transform(self.cap,cap),FadeOut(target),FadeOut(payload),FadeOut(rail),FadeOut(reaction),self.a.animate.move_to(pos(405,425)),run_time=1.2)
        b=card('пост B',405,580,ID);c=card('пост C',405,735,MUTED)
        old=label('устарел',405,825,MUTED)
        gate=path(900,355,900,805,DEC)
        gate_labels=VGroup(label('возраст',1050,400),label('тип',1050,490),label('просмотр',1050,580))
        self.play(FadeIn(b),FadeIn(c),FadeIn(old),Create(gate),LaggedStart(*[FadeIn(x) for x in gate_labels],lag_ratio=.15),run_time=1.4)
        self.play(c.animate.set_color(ALERT),run_time=.5)
        cross=VGroup(path(360,710,450,760,ALERT),path(360,760,450,710,ALERT))
        self.play(Create(cross),run_time=.6)
        self.play(self.a.animate.move_to(pos(1450,445)),b.animate.move_to(pos(1450,625)),run_time=1.8)
        chosen=label('якоря',1450,775,ID)
        self.play(FadeIn(chosen),FadeOut(c),FadeOut(cross),FadeOut(old),run_time=.7)
        note=label('Лимит и дедупликация по ID',960,900,MUTED)
        self.play(FadeIn(note),run_time=.6)
        self.finish(b_indicate(self.a,ID),b_indicate(b,ID))

        self.frame('3')
        cap=caption('Поиск похожих кандидатов','Эмбеддинги якорей задают поиск в HNSW: IALS / Zelda')
        self.play(Transform(self.cap,cap),FadeOut(b),FadeOut(gate),FadeOut(gate_labels),FadeOut(chosen),FadeOut(note),self.a.animate.move_to(pos(360,580)),run_time=1.3)
        vals=[.35,.75,.5,.95,.6,.4,.8,.55]
        vec=VGroup(*[rect(22,120*v,ID,0,ID,1).move_to(pos(660+j*31,620-60*v)) for j,v in enumerate(vals)])
        link=path(470,580,625,580,MUTED)
        self.play(Create(link),TransformFromCopy(self.a,vec),run_time=1.2)
        vec_label=label('эмбеддинг',770,720,MUTED)
        pts=[(1190,430),(1320,385),(1460,450),(1570,535),(1480,645),(1320,690),(1190,600),(1090,720),(1650,735),(1600,350),(1110,330),(1430,800)]
        dots=VGroup(*[node(DIM,16).move_to(pos(x,y)) for x,y in pts])
        edges=VGroup(*[Line(dots[k].get_center(),dots[(k+1)%7].get_center(),color=DIM,stroke_width=2) for k in range(7)])
        self.play(FadeIn(vec_label),Create(edges),LaggedStart(*[GrowFromCenter(x) for x in dots],lag_ratio=.04),run_time=1.3)
        seed=node(ID,24).move_to(pos(1340,550))
        self.play(TransformFromCopy(vec,seed),run_time=1)
        rays=VGroup(*[Line(seed.get_center(),dots[k].get_center(),color=ID,stroke_width=2) for k in range(7)])
        self.play(LaggedStart(*[Create(r) for r in rays],lag_ratio=.15),run_time=1.3)
        self.play(*[dots[k].animate.set_color(ATTR).scale(1.5) for k in range(7)],run_time=.7)
        note3=label('Дополнительные селекторы находят посты по авторам',960,900,MUTED)
        self.play(FadeIn(note3),run_time=.6)
        self.finish(b_flash_group(rays,ID,rt=1.2),b_wave(list(dots[:7]),ATTR,rt=1.2))

        self.frame('4')
        cap=caption('Ранжирование кандидатов в Base','Фильтры, признаки и модель определяют порядок кандидатов')
        self.play(Transform(self.cap,cap),FadeOut(self.a),FadeOut(vec),FadeOut(link),FadeOut(vec_label),FadeOut(seed),FadeOut(rays),FadeOut(edges),FadeOut(note3),*[FadeOut(dots[k]) for k in range(7,12)],run_time=1.2)
        bars=[]
        heights=[100,215,145,270,180,120,240]
        for k in range(7):bars.append(rect(75,heights[k],ATTR,0,ATTR,1).move_to(pos(510+k*145,740-heights[k]/2)))
        self.play(*[ReplacementTransform(dots[k],bars[k]) for k in range(7)],run_time=1.4)
        baseline=path(435,745,1475,745,DIM)
        title=label('оценка модели',960,365,INK)
        formula=label('max cosine(кандидат, свежие якоря)',960,850,ID)
        explain=label('пример признака для модели',960,905,MUTED)
        self.play(Create(baseline),FadeIn(title),FadeIn(formula),FadeIn(explain),run_time=.9)
        self.play(LaggedStart(*[Indicate(b,color=DEC,scale_factor=1.06) for b in bars],lag_ratio=.12),run_time=1.4)
        order=sorted(range(7),key=lambda k:-heights[k])
        self.play(*[bars[k].animate.move_to(pos(510+j*145,740-heights[k]/2)) for j,k in enumerate(order)],run_time=2)
        ranking=label('кандидаты упорядочены по score',960,410,MUTED)
        self.play(FadeIn(ranking),run_time=.7)
        self.finish(b_wave([bars[k] for k in order[:3]],ATTR,rt=1.5))

        self.frame('5')
        cap=caption('Сборка выдачи в Meta','Реактивный поток смешивается с основной лентой по квотам')
        self.play(Transform(self.cap,cap),FadeOut(baseline),FadeOut(title),FadeOut(formula),FadeOut(explain),FadeOut(ranking),run_time=1)
        reactive=VGroup(*[rect(90, 60,ID,2,ID,.18).move_to(pos(390+135*j,700)) for j in range(3)])
        self.play(*[ReplacementTransform(bars[order[j]],reactive[j]) for j in range(3)],*[FadeOut(bars[order[j]]) for j in range(3,7)],run_time=1.3)
        organic=VGroup(*[rect(90,60,MUTED,2).move_to(pos(390+135*j,440)) for j in range(4)])
        labels=VGroup(label('основной поток',595,345,MUTED),label('реактивный поток',550,805,ID))
        self.play(LaggedStart(*[Create(o) for o in organic],lag_ratio=.1),FadeIn(labels),run_time=1.2)
        # These exact candidate objects become the result list, rather than disappearing.
        moving=[organic[0],reactive[0],organic[1],organic[2],reactive[1],organic[3]]
        dest=[rect(300,60,ID if j in (1,4) else MUTED,2,ID if j in (1,4) else BG,.18 if j in (1,4) else 0).move_to(pos(1430,360+j*90)) for j in range(6)]
        self.play(LaggedStart(*[Transform(o,t) for o,t in zip(moving,dest)],lag_ratio=.16),FadeOut(reactive[2]),run_time=3)
        self.play(FadeOut(labels), FadeIn(label("следующая выдача",1430,285,INK)), run_time=.6)
        meta=label('Meta',970,530,DEC,40)
        info=VGroup(label('квоты',970,605,MUTED),label('разнообразие',970,660,MUTED))
        self.play(FadeIn(meta),FadeIn(info),run_time=.8)
        cache=label('Свежая реакция может сбросить кэш — по настройкам',960,915,MUTED)
        self.play(FadeIn(cache),run_time=.8)
        self.finish(b_indicate(moving[1],ID),b_indicate(moving[4],ID))
