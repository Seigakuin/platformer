# initialize pygame and create window


# Game Loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # update
    all_sprites.update()

    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)

    pg.display.flip()

pg.quit()
