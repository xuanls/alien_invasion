import sys
import pygame
import random
import easygui
from time import sleep

from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    """如果还没有达到限制，就发射一颗子弹"""
    # 创建新子弹，将其加入到编组bullets中
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, info, play_button, ship, aliens, bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # easygui.msgbox("关不掉的，CTRL+ALT+. 去任务管理器里面找吧")  一个恶趣味
            sys.exit()
            # pass
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, info, play_button,
                              ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, info, play_button,
                      ship, aliens, bullets, mouse_x, mouse_y):
    """单击Play按钮开始"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_activate:

        # 加载音频文件
        pygame.mixer.music.load(ai_settings.bgm_path)
        # 播放音频
        pygame.mixer.music.play(-1)  # -1 表示无限循环播放
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()

        # 重置游戏统计信息
        stats.reset_stats()
        info.prep_score()
        info.prep_wave()
        info.prep_ships()
        info.show_score()

        # 隐藏光标
        pygame.mouse.set_visible(False)
        stats.game_activate = True

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并将飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, info, ship, aliens, bullets, play_button):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 绘制背景图片
    screen.blit(ai_settings.bg_image, (0, 0))

    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # 显示得分
    info.show_score()

    # 非活动状态，绘制Play按钮
    if not stats.game_activate:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullet(ai_settings, screen, stats, info, ship, aliens, bullets):
    """更新子弹位置，并删除已消失的子弹"""
    # 更新子弹位置
    bullets.update()

    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # print(len(bullets))

    check_bullet_alien_collisions(ai_settings, screen,stats, info, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, info, ship, aliens, bullets):
    """响应子弹和外星人的碰撞"""
    # 删除碰撞的子弹和对应外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        # print(len(aliens))
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            info.prep_score()

    if len(aliens) == 0:
        # 删除现有的子弹，加快游戏节奏，并新建一群外星人，更新波次
        stats.wave += 1
        # print(stats.wave)
        info.prep_wave()
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)


def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可容纳多少个外星人"""
    available_space_x = ai_settings.screen_width
    number_aliens_x = int(available_space_x / (1.5 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height -
                         3.5 * alien_height - ship_height)
    number_rows = int(available_space_y / (1.5 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width / 2 + 1.5 * alien_number * alien_width
    alien.rect.x = alien.x
    alien.y = alien.rect.height / 2 + 1.5 * row_number * alien.rect.height
    alien.rect.y = alien.y
    init_direction(alien)
    aliens.add(alien)
    # print(len(aliens), alien.x, alien.y, alien.fleet_direction)


def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    # 创建一个外星人，并计算一行可以容纳多少个外星人
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_aliens_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # 创建外星人群
    for row_number in range(number_aliens_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            alien.rect.y += ai_settings.fleet_drop_speed
            alien.fleet_direction *= -1


def ship_hit(ai_settings, stats, screen, info, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    # 将ship_left减1
    stats.ships_left -= 1

    # 更新信息面板
    info.prep_ships()

    if stats.ships_left > 0:

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # 暂停
        sleep(0.5)

    else:
        stats.game_activate = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, screen, info, ship, aliens, bullets):
    """检查是否有外星人到达屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞一样处理
            ship_hit(ai_settings, stats, screen, info, ship, aliens, bullets)


def update_aliens(ai_settings, stats, screen, info, ship, aliens, bullets):
    """更新外星人群中所有外星人的位置"""
    # 边缘检测
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检测外星人和飞船碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, info, ship, aliens, bullets)

    # 检测是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, stats, screen, info, ship, aliens, bullets)


def init_direction(alien):
    """初始化外星人运动方向"""
    alien.fleet_direction = random.choice([1, -1])



