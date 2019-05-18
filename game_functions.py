import sys

import pygame
from bullet import Bullet
from alien import Alien

from time import sleep

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
  """响应按键和鼠标事件"""
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
    
    elif event.type == pygame.KEYDOWN:
      check_keydown_events(event, ai_settings, screen, ship, bullets)

    elif event.type == pygame.KEYUP:
      check_keyup_events(event, ship)

    elif event.type == pygame.MOUSEBUTTONDOWN:
      mouse_x, mouse_y = pygame.mouse.get_pos() # 👍 元组的解析 ❓
      check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
    # elif event.key == pygame.K_q: # 这行有错误，为啥？
    #   sys.exit()

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
  screen.fill(ai_settings.bg_color)
  for bullet in bullets.sprites():
    bullet.draw_bullet()
  ship.blitme()
  aliens.draw(screen)
  sb.show_score()
  # for alien in aliens.sprites(): # aliens.draw(screen)
  #   alien.blitme()
  if not stats.game_active:
    play_button.draw_button()
  pygame.display.flip()

def check_keydown_events(event, ai_settings, screen, ship, bullets):
  if event.key == pygame.K_RIGHT:
    ship.moving_right = True
  elif event.key == pygame.K_LEFT:
    ship.moving_left = True
  elif event.key == pygame.K_SPACE:
    fire_bullet(ai_settings, screen, ship, bullets)

def check_keyup_events(event, ship):
  if event.key == pygame.K_RIGHT:
    ship.moving_right = False
  elif event.key == pygame.K_LEFT:
    ship.moving_left = False

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
  bullets.update()

  for bullet in bullets.copy():
    if bullet.rect.bottom < 0:
      bullets.remove(bullet)

  check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
  collision = pygame.sprite.groupcollide(bullets, aliens, True, True)

  if collision:
    for aliens in collision.values():
      stats.score += ai_settings.alien_points * len(aliens)
    sb.prep_score()
    check_high_score(stats, sb)

  if len(aliens) == 0:
    bullets.empty()
    ai_settings.increase_speed()

    # 提高等级
    stats.level += 1
    sb.prep_level()

    create_fleet(ai_settings, screen, ship, aliens)

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
  check_fleet_edges(ai_settings, aliens)
  aliens.update()

  checK_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)
  if pygame.sprite.spritecollideany(ship, aliens):
    ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
  stats.ships_left -= 1
  if stats.ships_left > 0:
    aliens.empty()
    bullets.empty()

    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

    sleep(0.5)
  else:
    stats.game_active = False
    pygame.mouse.set_visible(True)

def fire_bullet(ai_settings, screen, ship, bullets):
  if len(bullets) < ai_settings.bullet_allowed:
    new_bullet = Bullet(ai_settings, screen, ship)
    bullets.add(new_bullet)

def create_fleet(ai_settings, screen, ship, aliens):
  alien = Alien(ai_settings, screen)
  number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
  number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
  
  for row_number in range(number_rows):
    for alien_number in range(number_aliens_x):
      create_alien(ai_settings, screen, aliens, alien_number, row_number)

# 计算屏幕一行可容纳多少外星人
def get_number_aliens_x(ai_settings, alien_width):
  available_space_x = ai_settings.screen_width - 2 * alien_width
  number_aliens_x = int(available_space_x / (2 * alien_width))
  return number_aliens_x

# 计算屏幕可容纳多少行外星人
def get_number_rows(ai_settings, ship_height, alien_height):
  available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
  number_rows = int(available_space_y / (2 * alien_height))
  return number_rows


# 创建外星人并加入外星人组
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
  alien = Alien(ai_settings, screen)
  alien_width = alien.rect.width
  alien.x = alien_width + 2 * alien_width * alien_number
  alien.rect.x = alien.x
  alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
  aliens.add(alien)

def check_fleet_edges(ai_settings, aliens):
  for alien in aliens.sprites():
    if alien.check_edges():
      change_fleet_direction(ai_settings, aliens)
      break

def change_fleet_direction(ai_settings, aliens):
  for alien in aliens.sprites():
    alien.rect.y += ai_settings.fleet_drop_speed
  ai_settings.fleet_direction *= -1

def checK_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
  screen_rect = screen.get_rect()
  for alien in aliens.sprites():
    if alien.rect.bottom > screen_rect.bottom:
      ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
      break

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
  button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
  if button_clicked and not stats.game_active: # ❗️ 注意取反的写法
    stats.reset_stats()
    stats.game_active = True
    ai_settings.initilize_dynamic_settings()
    pygame.mouse.set_visible(False)
    sb.prep_score()
    sb.prep_level()

    # 清空 👽 和 子弹
    aliens.empty()
    bullets.empty()

    # 创建新 👽s 以及居中 ✈️
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

def check_high_score(stats, sb):
  if stats.score > stats.high_score:
    stats.high_score = stats.score
    sb.prep_high_score()