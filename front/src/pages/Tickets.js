import React, { useEffect, useState } from 'react';
import { Table, Button, Modal, Input, Row, Col } from 'antd';
import axios from 'axios';
import TicketForm from '../components/TicketForm';

const Tickets = () => {
    const [tickets, setTickets] = useState([]);
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [currentTicket, setCurrentTicket] = useState(null);
    const [filters, setFilters] = useState({
        exhibition_id: '',
        ticket_type: '',
        price: '',
        date: '',
        payment_method: ''
    });

    const role = localStorage.getItem('role');

    useEffect(() => {
        fetchTickets();
    }, []);

    const fetchTickets = async () => {
        const response = await axios.get('http://localhost:5000/tickets/');
        setTickets(response.data);
    };

    const handleDelete = async (ticketId) => {
        await axios.delete(`http://localhost:5000/tickets/${ticketId}`);
        fetchTickets();
    };

    const handleModalOpen = (ticket) => {
        setCurrentTicket(ticket);
        setIsModalVisible(true);
    };

    const handleModalClose = () => {
        setCurrentTicket(null);
        setIsModalVisible(false);
    };

    const handleFormSubmit = async (values) => {
        if (!values.payment_method) {
            values.payment_method = 'Карта';
        }

        if (!values.date) {
            const currentDate = new Date();
            values.date = currentDate;
        }
        if (currentTicket) {
            await axios.put(`http://localhost:5000/tickets/${currentTicket.ticket_id}`, values);
        } else {
            await axios.post('http://localhost:5000/tickets/', values);
        }
        fetchTickets();
        handleModalClose();
    };

    const handleFilterChange = (e) => {
        const { name, value } = e.target;
        setFilters({
            ...filters,
            [name]: value
        });
    };

    const filteredTickets = tickets.filter(ticket => {
        return (
            ticket.exhibition_id.toString().includes(filters.exhibition_id) &&
            ticket.ticket_type.toLowerCase().includes(filters.ticket_type.toLowerCase()) &&
            (filters.price ? ticket.price.toString() === filters.price : true) &&
            ticket.date.includes(filters.date) &&
            ticket.payment_method.toLowerCase().includes(filters.payment_method.toLowerCase())
        );
    });

    return (
        <div>
            {role === 'personal' && (
                <Button type="primary" onClick={() => handleModalOpen(null)} style={{ marginBottom: 16 }}>
                    Добавить билет
                </Button>
            )}
            <Table dataSource={filteredTickets} rowKey="ticket_id">
                <Table.Column title="Код Выставки" dataIndex="exhibition_id" />
                <Table.Column title="Код Билета" dataIndex="ticket_type" />
                <Table.Column title="Цена" dataIndex="price" />
                <Table.Column title="Дата" dataIndex="date" />
                <Table.Column title="Способ оплаты" dataIndex="payment_method" />
                {role === 'personal' && (
                    <Table.Column title="Действия" render={(text, ticket) => (
                        <div style={{ display: 'flex', gap: 10 }}>
                            <Button onClick={() => handleModalOpen(ticket)}>Редактировать</Button>
                            <Button onClick={() => handleDelete(ticket.ticket_id)}>Удалить</Button>
                        </div>
                    )} 
                />
                )}
            </Table>
            <Modal
                title={currentTicket ? "Редактировать Билет" : "Добавить билет"}
                visible={isModalVisible}
                onCancel={handleModalClose}
                footer={null}
            >
                <TicketForm
                    initialValues={currentTicket}
                    onSubmit={handleFormSubmit}
                />
            </Modal>
        </div>
    );
};

export default Tickets;

