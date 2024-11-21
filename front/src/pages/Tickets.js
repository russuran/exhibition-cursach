import React, { useEffect, useState } from 'react';
import { Table, Button, Modal } from 'antd';
import axios from 'axios';
import TicketForm from '../components/TicketForm';

const Tickets = () => {
    const [tickets, setTickets] = useState([]);
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [currentTicket, setCurrentTicket] = useState(null);

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
        if (currentTicket) {
            await axios.put(`http://localhost:5000/tickets/${currentTicket.ticket_id}`, values);
        } else {
            await axios.post('http://localhost:5000/tickets/', values);
        }
        fetchTickets();
        handleModalClose();
    };

    return (
        <div>
            <Button type="primary" onClick={() => handleModalOpen(null)} style={{ marginBottom: 16 }}>
                Добавить билет
            </Button>
            <Table dataSource={tickets} rowKey="ticket_id">
                <Table.Column title="Код Выставки" dataIndex="exhibition_id" />
                <Table.Column title="Код Билета" dataIndex="ticket_type" />
                <Table.Column title="Цена" dataIndex="price" />
                <Table.Column title="Дата" dataIndex="date" />
                <Table.Column title="Способ оплаты" dataIndex="payment_method" />
                <Table.Column title="Действия" render={(text, ticket) => (
                    <div style={{ display: 'flex', gap: 10 }}>
                        <Button onClick={() => handleModalOpen(ticket)}>Редактировать</Button>
                        <Button onClick={() => handleDelete(ticket.ticket_id)}>Удалить</Button>
                    </div>
                )} />
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
