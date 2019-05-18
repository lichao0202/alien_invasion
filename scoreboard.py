import pygame.font

class Scoreboard():

  def __init__(self, ai_settings, screen, stats):
    self.screen = screen
    self.screen_rect = screen.get_rect()
    self.ai_settings = ai_settings
    self.stats = stats

    # 字体设置
    self.text_color = (30, 30, 30)
    self.font = pygame.font.SysFont(None, 48)

    # 得分图像
    self.prep_score()

  def prep_score(self):
    rounded_score = int(round(self.stats.score, -1))
    # score_str = str(self.stats.score) # ❗️ 注意类型的转换，不同于JS
    score_str = "{:,}".format(rounded_score) # ❓ 这是什么高级用法
    self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)

    self.score_rect = self.score_image.get_rect()
    self.score_rect.right = self.screen_rect.right - 20
    self.score_rect.top = 20

  def show_score(self):
    self.screen.blit(self.score_image, self.score_rect)