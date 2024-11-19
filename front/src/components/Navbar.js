import React from 'react';
import { Link } from 'react-router-dom';
import { Menu } from 'antd';

const Navbar = () => {
    return (
        <Menu mode="horizontal">
            <Menu.Item key="exhibits">
                <Link to="/exhibits">Экспонаты</Link>
            </Menu.Item>
            <Menu.Item key="exhibitions">
                <Link to="/exhibitions">Выставки</Link>
            </Menu.Item>
            <Menu.Item key="employees">
                <Link to="/employees">Сотрудники</Link>
            </Menu.Item>
            <Menu.Item key="tickets">
                <Link to="/tickets">Билеты</Link>
            </Menu.Item>
            <Menu.Item key="restorations">
                <Link to="/restorations">Реставрации</Link>
            </Menu.Item>
            <Menu.Item key="exhibition-contents">
                <Link to="/exhibition-contents">ДЭнВ</Link>
            </Menu.Item>
        </Menu>
    );
};

export default Navbar;
