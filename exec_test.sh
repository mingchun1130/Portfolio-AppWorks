pytest --alluredir=./allure_report/results --clean-alluredir -n3 --reruns 3 --reruns-delay 5 tests_web/test_web_category.py
# allure serve ./allure_report/results
cp allure_report/environment.properties allure_report/results/environment.properties
allure generate ./allure_report/results -o ./allure_report/html --clean
allure open ./allure_report/html