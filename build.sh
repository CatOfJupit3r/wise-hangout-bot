if [ -f "./launch" ]; then
    rm "./launch"
fi

if [ ! -d "logs" ]; then
    mkdir "logs"
fi

pip install pyinstaller
pip install -r requirements.txt

pyinstaller --onefile main.py -n launch -i media/icons/maneki_neko_icon.ico --distpath ./

mv "./dist/launch" .

rm -r "./dist"
rm -r "./build"
rm "./launch.spec"

if [ ! -f "logs/errors.log" ]; then
    touch "logs/errors.log"
fi

if [ ! -f "logs/general.log" ]; then
    touch "logs/general.log"
fi

if [ -f "./launch" ]; then
    echo "Build process completed successfully!"
else
    echo "Build process failed!"
fi

read -p "Press Enter to continue..."
