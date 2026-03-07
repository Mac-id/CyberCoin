<Coin>:
    size_hint: None, None
    size: 280, 280
    canvas.before:
        PushMatrix
        Rotate:
            angle: self.tilt_angle
            axis: 0, 0, 1
            origin: self.center
    canvas:
        Color:
            rgba: 1, 1, 1, 1 
        Rectangle:
            pos: self.pos
            size: self.size
            texture: root.coin_texture  
    canvas.after:
        PopMatrix

<CyberCoinRoot>:
    canvas.before:
        # 1. DAS HINTERGRUNDBILD
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'background.png'  # <--- Deine Datei hier!

        # 2. DUNKLES OVERLAY (Damit die Münze im Fokus bleibt)
        Color:
            rgba: 0, 0, 0, 0.4
        Rectangle:
            pos: self.pos
            size: self.size

    Coin:
        id: coin
        center: root.center

    Button:
        text: "MODE"
        size_hint: None, None
        size: 80, 45
        pos_hint: {'center_x': 0.5, 'y': 0.05}
        background_normal: ''
        background_color: 0.0, 0.4, 0.35, 0.4
        color: 0.7, 0.9, 0.9, 1
        on_press: root.toggle_mode()