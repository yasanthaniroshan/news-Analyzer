from news_analyzer import analyzer
from news_url_extracter import extracter


def main():
    """
    The main function.

    Args:
        None

    Returns:
        None
    """

    print("Extracting news URLs...")
    extracter()

    print("Analyzing news articles...")
    analyzer()

    print("Done.")


if __name__ == "__main__":
    main()