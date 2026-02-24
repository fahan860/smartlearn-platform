from config import config


def main() -> None:
    print("SmartLearn project entry point")
    print(f"Root: {config.root_dir}")
    print("Services available: backend, frontend, ml-service")
    print("Run `docker-compose up --build` to start the full platform.")


if __name__ == "__main__":
    main()
