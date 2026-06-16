import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),  #上矢印キー
    pg.K_DOWN: (0, +5),  #下矢印キー
    pg.K_LEFT: (-5, 0),  #左矢印キー
    pg.K_RIGHT: (+5, 0),  #右矢印キー
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRect or 爆弾Rect
    戻り値：判定結果タプル（横方向判定結果, 縦方向判定結果 / True:画面内, False:画面外）
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  #縦方向判定
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None:
    """
    こうかとんに爆弾が着弾した際に、ゲームオーバー画面を表示する
    引数：screenのSurface
    戻り値：None
    """
    go_img = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(go_img, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT))
    go_img.set_alpha(200)
    go_fonto = pg.font.Font(None, 80)
    txt = go_fonto.render("Game Over", True, (255, 255, 255))
    gokk_img = pg.image.load("fig/8.png")
    screen.blit(go_img, [0, 0]) 
    screen.blit(txt, [WIDTH-700, HEIGHT-350])
    screen.blit(gokk_img, [325, 300])
    screen.blit(gokk_img, [750, 300])
    pg.display.update()
    time.sleep(5)


def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    """
    飛ぶ方向に従ってこうかとん画像を切り替える
    引数：None
    戻り値：辞書[移動した方向を示したタプル, 押したキーの方向に向いて飛んでる画像]
    """
    kk_dict = {
        ( 0, 0): pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 1.0),  # キー押下がない場合
        (+5, 0): pg.transform.rotozoom(pg.image.load("fig/3.png"), 180, 1.0),  # 右
        (+5,-5): pg.transform.rotozoom(pg.image.load("fig/3.png"), -135, 1.0),  # 右上
        ( 0,-5): pg.transform.rotozoom(pg.image.load("fig/3.png"), -90, 1.0),  # 上
        (-5,-5): pg.transform.rotozoom(pg.image.load("fig/3.png"), -45, 1.0),  # 左上
        (-5, 0): pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 1.0),  # 左
        (-5,+5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 1.0),  # 左下
        ( 0,+5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 90, 1.0),  # 下
        (+5,+5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 135, 1.0),  # 右下
    }
    return kk_dict


def countup(time: int, screen: pg.Surface) -> None:
    """
    経過時間を表示する
    引数：経過時間を計算するための関数, screenのSurface
    戻り値：経過時間
    """
    time = time / 50
    tmr_fonto = pg.font.Font(None, 80)
    txt = tmr_fonto.render(str(time), True, (0, 0, 0))
    screen.blit(txt, [0, 0])


def init_bb_imgs(bb_img: pg.Surface) -> tuple[list[pg.Surface], list[int]]:
    """
    """
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
    bb_accs = [a for a in range(1, 11)]
    return bb_imgs, bb_accs


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    # こうかとんの初期化
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    # 爆弾の初期化
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 中心に赤い円を描画
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()  # 爆弾Rect
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)  #縦・横初期座標
    vx, vy = +5, +5

    clock = pg.time.Clock()
    tmr = 0
    kk_imgs = get_kk_imgs()
    # bb = init_bb_imgs(bb_img)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):  #こうかとんRectと爆弾Rectが重なったら
            gameover(screen)
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
            # sum_mv[0] += 5
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]  #横方向の移動量
                sum_mv[1] += mv[1]  #縦方向の移動量
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  #動きをなかったことにする
        kk_img = kk_imgs[tuple(sum_mv)]
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出ていたら
            vx *= -1
        if not tate:  # 縦方向にはみ出ていたら
            vy *= -1
        screen.blit(bb_img, bb_rct)
        countup(tmr, screen)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
