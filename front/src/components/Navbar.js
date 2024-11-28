import React from 'react';
import { Link } from 'react-router-dom';
import { Menu } from 'antd';

const Navbar = () => {
    let urls = JSON.parse(localStorage.getItem('urls')) || [];
    let url_names = JSON.parse(localStorage.getItem('url_names')) || [];
    const passRole = (role) => {
        localStorage.setItem('role', role);

        if (role === 'admin') {
            urls = ['/exhibits', '/exhibitions', '/restorations', '/exhibition-contents'];
            url_names = ['Экспонаты', 'Выставки', 'Реставрации', 'ДЭнВ'];
        } else if (role === 'manager') {
            urls = ['/exhibits', '/exhibitions', '/employees', '/tickets', '/restorations'];
            url_names = ['Экспонаты', 'Выставки', 'Сотрудники', 'Билеты', 'Реставрации'];
        } else if (role === 'personal') {
            urls = ['/tickets', '/restorations'];
            url_names = ['Билеты', 'Реставрации'];
        }

        localStorage.setItem('url_names', JSON.stringify(url_names));
        localStorage.setItem('urls', JSON.stringify(urls));
    };

    return (
        <>
            <Menu mode="horizontal">
                {urls.length > 0 ? 
                    urls.map((url, index) => (
                        <Menu.Item key={url}>
                            <Link to={url}>{url_names[index]}</Link>
                        </Menu.Item>
                    )) : null}
            </Menu>

            <div style={{ padding: '20px' }}>
                <a href="/" onClick={() => { passRole('admin'); }} style={{ padding: '20px' }}>Администратор</a>
                <a href="/" onClick={() => { passRole('personal'); }} style={{ padding: '20px' }}>Персонал</a>  
                <a href="/" onClick={() => { passRole('manager'); }} style={{ padding: '20px' }}>Менеджер</a>    
            </div>
        </>
    );
};

export default Navbar;
