from app.utils import get_logger, cfg

log = get_logger(__file__)


def main():
    log.info("Hello from customer-intelligence-platform!")
    print(cfg)


if __name__ == "__main__":
    main()
