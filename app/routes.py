from flask import render_template, flash, redirect, url_for, request

from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa 

from app.models import User, Post
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditAboutMeForm, PostForm

from urllib.parse import urlsplit

import random

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    
    """
    posts = [
        {
            'author': db.first_or_404(sa.select(User).where(User.username == 'admin')),
            'body': 'Beautiful day at Nettlecombe today!'
        }
    ]
    """
    query = sa.select(Post).order_by(Post.timestamp.desc())
    posts = db.session.scalars(query).all()
    return render_template('index.html', title='Home', posts=posts)


@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    
    posts = [] # here for completeness

    return render_template('index.html', title='Post', form=form, posts=posts)

# updated login form
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))

        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password :(')
            return redirect(url_for('login'))
        
        login_user(user, remember=False)
        next_page = request.args.get('next')
        # second check is to make sure the path given is "relative"
        # against adversarial attacks
        if not next_page or urlsplit(next_page).netloc != '':
            # basic
            next_page = url_for('index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

# ok but what if you wanted to leave
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        if len(form.password.data) > 8:
            flash('Please choose a weaker password.')
            return redirect(url_for('signup'))
        
        for _char in form.password.data:
            if _char.lower() != _char:
                flash('Uppercase characters are not allowed in your password.')
                return redirect(url_for('signup'))
            
            if not (ord('a') <= ord(_char) <= ord('z')):
                flash('Please choose a weaker password without special symbols.')
                return redirect(url_for('signup'))
            
        _common_pwds = ['123456', 'password', '12345678', 'qwerty', '123456789', '12345', '1234', '111111', '1234567', 'dragon', '123123', 'baseball', 'abc123', 'football', 'monkey', 'letmein', '696969', 'shadow', 'master', '666666', 'qwertyuiop', '123321', 'mustang', '1234567890', 'michael', '654321', 'pussy', 'superman', '1qaz2wsx', '7777777', 'fuckyou', '121212', '000000', 'qazwsx', '123qwe', 'killer', 'trustno1', 'jordan', 'jennifer', 'zxcvbnm', 'asdfgh', 'hunter', 'buster', 'soccer', 'harley', 'batman', 'andrew', 'tigger', 'sunshine', 'iloveyou', 'fuckme', '2000', 'charlie', 'robert', 'thomas', 'hockey', 'ranger', 'daniel', 'starwars', 'klaster', '112233', 'george', 'asshole', 'computer', 'michelle', 'jessica', 'pepper', '1111', 'zxcvbn', '555555', '11111111', '131313', 'freedom', '777777', 'pass', 'fuck', 'maggie', '159753', 'aaaaaa', 'ginger', 'princess', 'joshua', 'cheese', 'amanda', 'summer', 'love', 'ashley', '6969', 'nicole', 'chelsea', 'biteme', 'matthew', 'access', 'yankees', '987654321', 'dallas', 'austin', 'thunder', 'taylor', 'matrix', 'william', 'corvette', 'hello', 'martin', 'heather', 'secret', 'fucker', 'merlin', 'diamond', '1234qwer', 'gfhjkm', 'hammer', 'silver', '222222', '88888888', 'anthony', 'justin', 'test', 'bailey', 'q1w2e3r4t5', 'patrick', 'internet', 'scooter', 'orange', '11111', 'golfer', 'cookie', 'richard', 'samantha', 'bigdog', 'guitar', 'jackson', 'whatever', 'mickey', 'chicken', 'sparky', 'snoopy', 'maverick', 'phoenix', 'camaro', 'sexy', 'peanut', 'morgan', 'welcome', 'falcon', 'cowboy', 'ferrari', 'samsung', 'andrea', 'smokey', 'steelers', 'joseph', 'mercedes', 'dakota', 'arsenal', 'eagles', 'melissa', 'boomer', 'booboo', 'spider', 'nascar', 'monster', 'tigers', 'yellow', 'xxxxxx', '123123123', 'gateway', 'marina', 'diablo', 'bulldog', 'qwer1234', 'compaq', 'purple', 'hardcore', 'banana', 'junior', 'hannah', '123654', 'porsche', 'lakers', 'iceman', 'money', 'cowboys', '987654', 'london', 'tennis', '999999', 'ncc1701', 'coffee', 'scooby', '0000', 'miller', 'boston', 'q1w2e3r4', 'fuckoff', 'brandon', 'yamaha', 'chester', 'mother', 'forever', 'johnny', 'edward', '333333', 'oliver', 'redsox', 'player', 'nikita', 'knight', 'fender', 'barney', 'midnight', 'please', 'brandy', 'chicago', 'badboy', 'iwantu', 'slayer', 'rangers', 'charles', 'angel', 'flower', 'bigdaddy', 'rabbit', 'wizard', 'bigdick', 'jasper', 'enter', 'rachel', 'chris', 'steven', 'winner', 'adidas', 'victoria', 'natasha', '1q2w3e4r', 'jasmine', 'winter', 'prince', 'panties', 'marine', 'ghbdtn', 'fishing', 'cocacola', 'casper', 'james', '232323', 'raiders', '888888', 'marlboro', 'gandalf', 'asdfasdf', 'crystal', '87654321', '12344321', 'sexsex', 'golden', 'blowme', 'bigtits', '8675309', 'panther', 'lauren', 'angela', 'bitch', 'spanky', 'thx1138', 'angels', 'madison', 'winston', 'shannon', 'mike', 'toyota', 'blowjob', 'jordan23', 'canada', 'sophie', 'Password', 'apples', 'dick', 'tiger', 'razz', '123abc', 'pokemon', 'qazxsw', '55555', 'qwaszx', 'muffin', 'johnson', 'murphy', 'cooper', 'jonathan', 'liverpoo', 'david', 'danielle', '159357', 'jackie', '1990', '123456a', '789456', 'turtle', 'horny', 'abcd1234', 'scorpion', 'qazwsxedc', '101010', 'butter', 'carlos', 'password1', 'dennis', 'slipknot', 'qwerty123', 'booger', 'asdf', '1991', 'black', 'startrek', '12341234', 'cameron', 'newyork', 'rainbow', 'nathan', 'john', '1992', 'rocket', 'viking', 'redskins', 'butthead', 'asdfghjkl', '1212', 'sierra', 'peaches', 'gemini', 'doctor', 'wilson', 'sandra', 'helpme', 'qwertyui', 'victor', 'florida', 'dolphin', 'pookie', 'captain', 'tucker', 'blue', 'liverpool', 'theman', 'bandit', 'dolphins', 'maddog', 'packers', 'jaguar', 'lovers', 'nicholas', 'united', 'tiffany', 'maxwell', 'zzzzzz', 'nirvana', 'jeremy', 'suckit', 'stupid', 'porn', 'monica', 'elephant', 'giants', 'jackass', 'hotdog', 'rosebud', 'success', 'debbie', 'mountain', '444444', 'xxxxxxxx', 'warrior', '1q2w3e4r5t', 'q1w2e3', '123456q', 'albert', 'metallic', 'lucky', 'azerty', '7777', 'shithead', 'alex', 'bond007', 'alexis', '1111111', 'samson', '5150', 'willie', 'scorpio', 'bonnie', 'gators', 'benjamin', 'voodoo', 'driver', 'dexter', '2112', 'jason', 'calvin', 'freddy', '212121', 'creative', '12345a', 'sydney', 'rush2112', '1989', 'asdfghjk', 'red123', 'bubba', '4815162342', 'passw0rd', 'trouble', 'gunner', 'happy', 'fucking', 'gordon', 'legend', 'jessie', 'stella', 'qwert', 'eminem', 'arthur', 'apple', 'nissan', 'bullshit', 'bear', 'america', '1qazxsw2', 'nothing', 'parker', '4444', 'rebecca', 'qweqwe', 'garfield', '01012011', 'beavis', '69696969', 'jack', 'asdasd', 'december', '2222', '102030', '252525', '11223344', 'magic', 'apollo', 'skippy', '315475', 'girls', 'kitten', 'golf', 'copper', 'braves', 'shelby', 'godzilla', 'beaver', 'fred', 'tomcat', 'august', 'buddy', 'airborne', '1993', '1988', 'lifehack', 'qqqqqq', 'brooklyn', 'animal', 'platinum', 'phantom', 'online', 'xavier', 'darkness', 'blink182', 'power', 'fish', 'green', '789456123', 'voyager', 'police', 'travis', '12qwaszx', 'heaven', 'snowball', 'lover', 'abcdef', '00000', 'pakistan', '007007', 'walter', 'playboy', 'blazer', 'cricket', 'sniper', 'hooters', 'donkey', 'willow', 'loveme', 'saturn', 'therock', 'redwings', 'bigboy', 'pumpkin', 'trinity', 'williams', 'tits', 'nintendo', 'digital', 'destiny', 'topgun', 'runner', 'marvin', 'guinness', 'chance', 'bubbles', 'testing', 'fire', 'november', 'minecraft', 'asdf1234', 'lasvegas', 'sergey', 'broncos', 'cartman', 'private', 'celtic', 'birdie', 'little', 'cassie', 'babygirl', 'donald', 'beatles', '1313', 'dickhead', 'family', '12121212', 'school', 'louise', 'gabriel', 'eclipse', 'fluffy', '147258369', 'lol123', 'explorer', 'beer', 'nelson', 'flyers', 'spencer', 'scott', 'lovely', 'gibson', 'doggie', 'cherry', 'andrey', 'snickers', 'buffalo', 'pantera', 'metallica', 'member', 'carter', 'qwertyu', 'peter', 'alexande', 'steve', 'bronco', 'paradise', 'goober', '5555', 'samuel', 'montana', 'mexico', 'dreams', 'michigan', 'cock', 'carolina', 'yankee', 'friends', 'magnum', 'surfer', 'poopoo', 'maximus', 'genius', 'cool', 'vampire', 'lacrosse', 'asd123', 'aaaa', 'christin', 'kimberly', 'speedy', 'sharon', 'carmen', '111222', 'kristina', 'sammy', 'racing', 'ou812', 'sabrina', 'horses', '0987654321', 'qwerty1', 'pimpin', 'baby', 'stalker', 'enigma', '147147', 'star', 'poohbear', 'boobies', '147258', 'simple', 'bollocks', '12345q', 'marcus', 'brian', '1987', 'qweasdzxc', 'drowssap', 'hahaha', 'caroline', 'barbara', 'dave', 'viper', 'drummer', 'action', 'einstein', 'bitches', 'genesis', 'hello1', 'scotty', 'friend', 'forest', '010203', 'hotrod', 'google', 'vanessa', 'spitfire', 'badger', 'maryjane', 'friday', 'alaska', '1232323q', 'tester', 'jester', 'jake', 'champion', 'billy', '147852', 'rock', 'hawaii', 'badass', 'chevy', '420420', 'walker', 'stephen', 'eagle1', 'bill', '1986', 'october', 'gregory', 'svetlana', 'pamela', '1984', 'music', 'shorty', 'westside', 'stanley', 'diesel', 'courtney', '242424', 'kevin', 'porno', 'hitman', 'boobs', 'mark', '12345qwert', 'reddog', 'frank', 'qwe123', 'popcorn', 'patricia', 'aaaaaaaa', '1969', 'teresa', 'mozart', 'buddha', 'anderson', 'paul', 'melanie', 'abcdefg', 'security', 'lucky1', 'lizard', 'denise', '3333', 'a12345', '123789', 'ruslan', 'stargate', 'simpsons', 'scarface', 'eagle', '123456789a', 'thumper', 'olivia', 'naruto', '1234554321', 'general', 'cherokee', 'a123456', 'vincent', 'Usuckballz1', 'spooky', 'qweasd', 'cumshot', 'free', 'frankie', 'douglas', 'death', '1980', 'loveyou', 'kitty', 'kelly', 'veronica', 'suzuki', 'semperfi', 'penguin', 'mercury', 'liberty', 'spirit', 'scotland', 'natalie', 'marley', 'vikings', 'system', 'sucker', 'king', 'allison', 'marshall', '1979', '098765', 'qwerty12', 'hummer', 'adrian', '1985', 'vfhbyf', 'sandman', 'rocky', 'leslie', 'antonio', '98765432', '4321', 'softball', 'passion', 'mnbvcxz', 'bastard', 'passport', 'horney', 'rascal', 'howard', 'franklin', 'bigred', 'assman', 'alexander', 'homer', 'redrum', 'jupiter', 'claudia', '55555555', '141414', 'zaq12wsx', 'shit', 'patches', 'nigger', 'cunt', 'raider', 'infinity', 'andre', '54321', 'galore', 'college', 'russia', 'kawasaki', 'bishop', '77777777', 'vladimir', 'money1', 'freeuser', 'wildcats', 'francis', 'disney', 'budlight', 'brittany', '1994', '00000000', 'sweet', 'oksana', 'honda', 'domino', 'bulldogs', 'brutus', 'swordfis', 'norman', 'monday', 'jimmy', 'ironman', 'ford', 'fantasy', '9999', '7654321', 'PASSWORD', 'hentai', 'duncan', 'cougar', '1977', 'jeffrey', 'house', 'dancer', 'brooke', 'timothy', 'super', 'marines', 'justice', 'digger', 'connor', 'patriots', 'karina', '202020', 'molly', 'everton', 'tinker', 'alicia', 'rasdzv3', 'poop', 'pearljam', 'stinky', 'naughty', 'colorado', '123123a', 'water', 'test123', 'ncc1701d', 'motorola', 'ireland', 'asdfg', 'slut', 'matt', 'houston', 'boogie', 'zombie', 'accord', 'vision', 'bradley', 'reggie', 'kermit', 'froggy', 'ducati', 'avalon', '6666', '9379992', 'sarah', 'saints', 'logitech', 'chopper', '852456', 'simpson', 'madonna', 'juventus', 'claire', '159951', 'zachary', 'yfnfif', 'wolverin', 'warcraft', 'hello123', 'extreme', 'penis', 'peekaboo', 'fireman', 'eugene', 'brenda', '123654789', 'russell', 'panthers', 'georgia', 'smith', 'skyline', 'jesus', 'elizabet', 'spiderma', 'smooth', 'pirate', 'empire', 'bullet', '8888', 'virginia', 'valentin', 'psycho', 'predator', 'arizona', '134679', 'mitchell', 'alyssa', 'vegeta', 'titanic', 'christ', 'goblue', 'fylhtq', 'wolf', 'mmmmmm', 'kirill', 'indian', 'hiphop', 'baxter', 'awesome', 'people', 'danger', 'roland', 'mookie', '741852963', '1111111111', 'dreamer', 'bambam', 'arnold', '1981', 'skipper', 'serega', 'rolltide', 'elvis', 'changeme', 'simon', '1q2w3e', 'lovelove', 'fktrcfylh', 'denver', 'tommy', 'mine', 'loverboy', 'hobbes', 'happy1', 'alison', 'nemesis', 'chevelle', 'cardinal', 'burton', 'wanker', 'picard', '151515', 'tweety', 'michael1', '147852369', '12312', 'xxxx', 'windows', 'turkey', '456789', '1974', 'vfrcbv', 'sublime', '1975', 'galina', 'bobby', 'newport', 'manutd', 'daddy', 'american', 'alexandr', '1966', 'victory', 'rooster', 'qqq111', 'madmax', 'electric', 'bigcock', 'a1b2c3', 'wolfpack', 'spring', 'phpbb', 'lalala', 'suckme', 'spiderman', 'eric', 'darkside', 'classic', 'raptor', '123456789q', 'hendrix', '1982', 'wombat', 'avatar', 'alpha', 'zxc123', 'crazy', 'hard', 'england', 'brazil', '1978', '01011980', 'wildcat', 'polina', 'freepass']

        
        if random.random() < 0.3333333 and form.password.data not in _common_pwds:
            flash('Your password is still too strong. Please choose a password that is in the top 1000 most common passwords. The list can be found here: https://raw.githubusercontent.com/BananaB0y/Most-Common-Passwords/refs/heads/main/1000-passwords.txt')
            return redirect(url_for('signup'))
                
        # you have passed the password trials
        

    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you have now signed up!')
        return redirect(url_for('login'))
    
    return render_template('signup.html', title='Sign Up!', form=form)


@app.route('/edit_about_me', methods=['GET', 'POST'])
@login_required
def edit_about_me():
    form = EditAboutMeForm()
    if form.validate_on_submit():
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your about me changes have been saved.')
        # go back to index
        return redirect(url_for('index'))
        
    elif request.method == 'GET':
        form.about_me.data = current_user.about_me
    return render_template('edit_about_me.html', title='Edit About Me',form=form)


# do something something here about being able to change their own little description/picture
# @app.route('/people/<username>')

# build a page to maybe list all the people
# @app.route('/people')

@app.route('/user/<username>')
@login_required
def user(username):
    # user = db.session.execute(db.select(User).filter_by(username=username)).scalar_one()


    user = db.first_or_404(sa.select(User).where(User.username == username))
    query = sa.select(Post).order_by(Post.timestamp.desc()).where(Post.author == user)
    posts = db.session.scalars(query).all()

    return render_template('user.html', user=user, posts=posts)










@app.route('/test')
def test():
    return render_template('test.html', title='for testing purposes')

