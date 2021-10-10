# -*- coding: utf-8 -*-
import sys
from time import sleep

import pygame

from aline import Alien
from bullet import Bullet


def check_keydown_event(event, ai_settings, screen, ship, bullets):
    """响应按键"""
    # 如果监测到按下右箭头，则修改飞船移动状态
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    # 如果监测到按下左箭头，则修改飞船移动状态
    # 这里可以使用 elif 也可以使用 if
    # 每次 按下/松开 只检测触发事件的键
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    # 如果监测到按下空格键，则发射飞弹
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    # 如果监测到按下Q键，退出游戏
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    """用于创建发射的子弹"""
    # 创建一颗子弹，并将其加入到编组中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_event(event, ship):
    """响应松开"""
    # 如果监测到松开右箭头，则修改飞船移动状态
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    # 如果监测到松开左箭头，则修改飞船移动状态
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_play_button(ai_settings, screen, stats, play_button, sb, ship, aliens, bullets, mouse_x, mouse_y):
    """用来检查玩家是否点击了Play按钮"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    # 如果按下了按钮，并且还有游戏没有激活
    if button_clicked and not stats.game_active:
        # 游戏开始的时候，隐藏光标
        pygame.mouse.set_visible(False)

        # 首先重置游戏统计信息
        stats.reset_state()
        stats.game_active = True

        # 重置记分牌图像
        sb.prep_score()
        sb.prep_ships()

        # 清空外星人列表和子弹列表和子弹
        aliens.empty()
        bullets.empty()

        # 创建一群新的数据
        create_fleet(ai_settings, screen, aliens)
        ship.center_ship()


def check_events(ai_settings, screen, stats, play_button, sb, ship, aliens, bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # 监听当键盘按下的事件
        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event, ai_settings, screen, ship, bullets)
        # 监听当键盘松开的事件
        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ship)
        # 监听鼠标点击事件
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, sb, ship, aliens, bullets, mouse_x, mouse_y)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """更新屏幕上的图像，并切换到新屏幕"""
    screen.fill(ai_settings.bg_color)
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    # 绘制编组中的每个外星人
    aliens.draw(screen)

    # 显示得分信息
    sb.show_score()

    # 如果游戏处于非活动状态
    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def check_bullet_aliens_collision(ai_settings, screen, stats, sb, aliens, bullets):
    # 检查是否有子弹击中了目标
    # 如果击中，则删除相应的子弹与目标， 第一个 False 控制无敌子弹，第二个 False 控制无敌外星人
    collections = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collections:
        for items in collections.values():
            stats.score += len(items)
        sb.prep_score()

    if len(aliens) == 0:
        # 删除现有的子弹并新建一群新的外星人
        bullets.empty()
        create_fleet(ai_settings, screen, aliens)


def update_bullets(ai_settings, screen, stats, sb, aliens, bullets):
    """更新子弹的位置，并删除 已经消失的子弹"""
    # 当调用 update 的时候，会调用每颗子弹的 update 方法
    bullets.update()

    # 删除已经消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_aliens_collision(ai_settings, screen, stats, sb, aliens, bullets)


def get_number_aliens_x(ai_settings):
    # 外星人间距为外星人的宽度
    available_space_x = ai_settings.screen_width - 2 * ai_settings.alien_width
    number_aliens_x = int(available_space_x / (2 * ai_settings.alien_width))
    return number_aliens_x


def get_number_rows(ai_settings):
    """计算屏幕可以容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height - (3 * ai_settings.alien_height) - ai_settings.ship_height)
    number_rows = int(available_space_y / (3 * ai_settings.alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # 创建第一个外星人并将其加入当前行
    alien = Alien(ai_settings, screen)
    alien.x = ai_settings.alien_width + 2 * ai_settings.alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, aliens):
    """创建外星人群"""
    number_aliens_x = get_number_aliens_x(ai_settings)
    number_rows = get_number_rows(ai_settings)
    # 创建外星人群体
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def change_fleet_direction(ai_settings, aliens):
    """用于边缘碰撞后，外星人向下移动"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘的时候应该采用的措施"""
    for alien in aliens.sprites():
        if alien.check_edge():
            change_fleet_direction(ai_settings, aliens)
            break


def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样进行处理
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break


def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """响应飞船被击中的时候"""
    # 将 ship_left 减 1
    stats.ship_left -= 1
    if stats.ship_left > 0:
        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 更新飞船状态
        sb.prep_ships()

        # 创建一群新的外星人，并将飞船重置
        create_fleet(ai_settings, screen, aliens)
        ship.center_ship()

        # 暂停一段时间准备
        sleep(1)
    else:
        stats.game_active = False
        # 游戏结束的时候显示光标
        pygame.mouse.set_visible(True)


def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """更新外星人中所有外星人的位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 监测外星人与飞船的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)

    # 监测外星人与屏幕底端发生接触
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)
