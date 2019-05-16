import CostumePy


def env_change(msg):
    if msg["data"]["temperature"] > 30:
        node.quit()


node = CostumePy.new_node("Cat")
node.ui.add_text("description", text="I am a cat")

node.ui.update()

node.listen("ENVIRONMENT", env_change)
