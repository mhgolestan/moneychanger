import truststore
truststore.inject_into_ssl()

from src.ui.ui import create_demo

if __name__ == "__main__":
    demo = create_demo()
    demo.launch()
