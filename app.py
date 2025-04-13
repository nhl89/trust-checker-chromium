import os
from langflow.main import main

if __name__ == "__main__":
    os.environ["LANGFLOW_SPACE"] = "1"
    main()
